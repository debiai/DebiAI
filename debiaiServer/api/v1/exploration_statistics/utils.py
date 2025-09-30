from debiaiServer.modules.dataProviders.DataProvider import DataProvider
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
from pickledb import PickleDB
import uuid
from typing import Any, List, Dict

# Create or load a database
project_explorations_db = PickleDB("projectsExplorationsStatistics.db")


# Statistics
def set_column_type(column) -> str:
    # Return mixed if the column has more than one type
    # Except if the column has numbers and text
    nb_types = 0

    if ("hasNumbers" in column["tags"]) or ("hasText" in column["tags"]):
        nb_types += 1
    if "hasList" in column["tags"]:
        nb_types += 1
    if "hasDict" in column["tags"]:
        nb_types += 1
    if nb_types > 1:
        return "mixed"

    # Return the type of the column
    # text overrides number
    if "hasText" in column["tags"]:
        return "text"
    if "hasNumbers" in column["tags"]:
        return "number"
    if "hasList" in column["tags"]:
        return "list"
    if "hasDict" in column["tags"]:
        return "dict"

    return "other"


def can_calculate(column):
    # Check if the column can be calculated
    # Only columns that have numbers or text can be calculated
    if "hasNumbers" in column["tags"] and not (
        "hasText" in column["tags"]
        or "hasOther" in column["tags"]
        or "hasList" in column["tags"]
        or "hasDict" in column["tags"]
    ):
        return True
    return False


def get_columns_statistics(dataProviderId, projectId):
    SAMPLES_PER_PAGE = 50000

    print(f" - Getting columns statistics for project {projectId} on {dataProviderId}")

    # To remove during V0 legacy API removal in future versions
    if dataProviderId == "json_block":
        dataProviderId = "Python module Data Provider"

    # Find the data provider & project
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    data_provider_project = data_provider.get_project(projectId)

    # Check if we already have the statistics
    project_columns_statistics_db_key = f"{dataProviderId}_{projectId}"
    existing = project_explorations_db.get(project_columns_statistics_db_key)
    if existing:
        # Get the project update time
        project_update_time = data_provider_project.get("updateDate", 0)
        if type(existing) is dict:
            existing_update_time = existing.get("updateDate", 0)
            if existing_update_time >= project_update_time:
                return {"columns": existing["columns"]}

    # Get the project columns structure
    print(" - Getting columns structure")
    columns_structure = data_provider_project["columns"]
    # [
    #     {"name": "image", "category": "other", "type": "auto"},
    #     {"name": "objects", "category": "groundtruth", "type": "list"},
    #     {"name": "camera", "category": "context", "type": "text"},
    #     {"name": "objects number", "category": "context", "type": "number"},
    #     {"name": "per classes number", "category": "context", "type": "number"},
    # ]

    # In the structure we have the following elements
    # - name
    # - type
    # - tags (list of tags among which)
    #       "hasNumbers"
    #       "hasText"
    #       "hasNull"
    #       "hasList"
    #       "hasDict"
    #       "hasOther"
    # - metadata (list of information)
    #       "category" : => if not define <=> auto
    # - metrics (list of columns metrics)
    #       - NbUniques
    #       - ...
    #
    # Set the columns statistics
    columns_statistics = []
    for column in columns_structure:
        # Get the column statistics
        column_statistics = {
            "name": column["name"],
            "type": column["type"],
            "tags": [],
            "metadata": {
                "category": column["category"],
            },
            "metrics": {
                "nbUniqueValues": 0,
                "nbNullValues": 0,
                "average": None,
                "min": None,
                "max": None,
            },
        }
        columns_statistics.append(column_statistics)

    # Get the columns statistics
    analysis_id = str(uuid.uuid4())
    unique_values_map = {}
    nb_samples = 0

    print(" - Getting samples id list")

    while True:
        # Get the samples id list
        analysis = {"id": analysis_id, "first": nb_samples == 0, "last": False}
        data_id_list = data_provider.get_id_list(
            projectId,
            analysis,
            nb_samples,
            nb_samples + SAMPLES_PER_PAGE - 1,
        )

        # Load the samples
        analysis = {
            "id": analysis_id,
            "first": nb_samples == 0,
            "last": False,
        }

        # Get the samples
        data = data_provider.get_samples(projectId, analysis, data_id_list)

        # Do some statistics on the samples
        current_sample_nb = nb_samples
        for sample_id, sample_values in data.items():
            # For each value in the sample
            for value_index, sample in enumerate(sample_values):
                current_sample_nb += 1
                # Get the column
                column = columns_statistics[value_index]

                # Check if the column value is None
                if sample is None:
                    if "hasNull" not in column["tags"]:
                        column["tags"].append("hasNull")
                    column["metrics"]["nbNullValues"] += 1
                    continue

                # Check the sample type
                if isinstance(sample, (int, float)):
                    if "hasNumbers" not in column["tags"]:
                        column["tags"].append("hasNumbers")
                elif isinstance(sample, str):
                    if "hasText" not in column["tags"]:
                        column["tags"].append("hasText")
                elif isinstance(sample, list):
                    if "hasList" not in column["tags"]:
                        column["tags"].append("hasList")
                elif isinstance(sample, dict):
                    if "hasDict" not in column["tags"]:
                        column["tags"].append("hasDict")
                else:
                    print("Unknown type", type(sample))
                    if "hasOther" not in column["tags"]:
                        column["tags"].append("hasOther")

                # Deal with the unique values
                if "hasNumbers" in column["tags"] or "hasText" in column["tags"]:
                    if column["name"] not in unique_values_map:
                        unique_values_map[column["name"]] = set()
                    unique_values_map[column["name"]].add(sample)

                # Update the min, max and average
                if can_calculate(column):
                    # Update the min, max and average
                    if (
                        column["metrics"]["min"] is None
                        or sample < column["metrics"]["min"]
                    ):
                        column["metrics"]["min"] = sample
                    if (
                        column["metrics"]["max"] is None
                        or sample > column["metrics"]["max"]
                    ):
                        column["metrics"]["max"] = sample
                    if column["metrics"]["average"] is None:
                        column["metrics"]["average"] = sample
                    else:
                        column["metrics"]["average"] = (
                            column["metrics"]["average"] * (current_sample_nb - 1)
                            + sample
                        ) / current_sample_nb

        # If no more samples, break the loop
        nb_samples += len(data_id_list)
        print("  - nb_samples", nb_samples)
        if len(data_id_list) < SAMPLES_PER_PAGE:
            break

    # Final processing of the columns statistics
    for column in columns_statistics:
        # Set the unique values nb
        # Skip the columns that are not of type number or text
        if column["name"] in unique_values_map and not (
            "hasDict" in column["tags"]
            or "hasList" in column["tags"]
            or "hasOther" in column["tags"]
        ):
            column["metrics"]["nbUniqueValues"] = len(unique_values_map[column["name"]])

        # Set the type of the column
        column["type"] = set_column_type(column)

    # Save the statistics in the database
    project_explorations_db.set(
        project_columns_statistics_db_key,
        {
            "dataProviderId": dataProviderId,
            "projectId": projectId,
            "columns": columns_statistics,
            "updateDate": data_provider_project["updateDate"],
        },
    )
    project_explorations_db.save()

    return {"columns": columns_statistics}


# Data loaders
def get_samples_batch(
    data_provider: DataProvider, projectId, analysis, start, end
) -> dict:
    # Get the samples id list
    data_id_list = data_provider.get_id_list(
        projectId,
        analysis,
        start,
        end,
    )

    # Load the samples
    data = data_provider.get_samples(projectId, analysis, data_id_list)

    return data


def get_column_value_in_data(
    column_name: str, sample_data: list, project_columns: list
) -> Any:
    for i, column in enumerate(project_columns):
        if column["name"] == column_name:
            return sample_data[i]
    raise ValueError(f"Column '{column_name}' not found in project columns.")


def get_samples_batch_by_columns(
    data_provider: DataProvider,
    projectId,
    analysis,
    start,
    end,
    project_columns: list,
    selected_columns: list,
    selected_columns_aggregations: dict,
) -> dict:
    """
    Returns a { column_name: [value1, value2, ...] }
    dictionary for the samples in the given range.
    """

    # Get the samples arrays
    data = get_samples_batch(data_provider, projectId, analysis, start, end)

    # Data:
    # {
    #     "sample_id": [
    #         "Value1",
    #         2,
    #         [...],
    #         ...
    #     ],
    #     ...
    # }

    # Get the index of the selected columns in the project columns
    column_indices = {
        column["name"]: i
        for i, column in enumerate(project_columns)
        if column["name"] in selected_columns
    }

    # Convert to a dictionary with column names as keys
    data_columns = {}
    for column_name in selected_columns:
        data_columns[column_name] = [None] * len(data)
        for data_index, sample_data in enumerate(data.values()):
            data_columns[column_name][data_index] = sample_data[
                column_indices[column_name]
            ]

    return data_columns


def get_data_batch(
    data_provider: DataProvider,
    projectId,
    analysis,
    start,
    end,
    project_columns: list,
    selected_columns_labels: List[str],
    columns_aggregation_config: dict,
    columns_statistics: dict,
    metric_columns_to_fetch: list,
) -> Dict[str, dict]:
    """
    Returns a value for each data for the combinations:
    {
        "dataId1": {
            "column_values": [1, "A"],
            "metric_column_values": {
                "col1": 0.5,
                "col2": 1.0,
            },
        },
        "dataId2": {
            "column_values": [2, "B"],
            "metric_column_values": {
                "col1": 0.7,
                "col2": 1.2,
            },
        },
        ...
    }
    """

    # Get the samples arrays
    data = get_samples_batch(data_provider, projectId, analysis, start, end)

    # Data:
    # {
    #     "sample_id": [
    #         "Value1",
    #         2,
    #         [...],
    #         ...
    #     ],
    #     ...
    # }

    # Get the index of the selected columns in the project columns
    column_indices = {
        column["name"]: i
        for i, column in enumerate(project_columns)
        if column["name"] in selected_columns_labels
    }
    metric_column_indices = {
        column["name"]: i
        for i, column in enumerate(project_columns)
        if column["name"] in metric_columns_to_fetch
    }

    # Convert to a dictionary with data id as keys
    data_columns = {}
    for data_id, sample_data in data.items():
        data_columns[data_id] = {
            "column_values": tuple(
                [
                    apply_aggregations(
                        sample_data[column_indices[column_name]],
                        column_name,
                        columns_aggregation_config,
                        columns_statistics,
                    )
                    for column_name in selected_columns_labels
                ]
            ),
            "metric_column_values": {},
        }

        for metric_column_name in metric_columns_to_fetch:
            metric_value = sample_data[metric_column_indices[metric_column_name]]
            data_columns[data_id]["metric_column_values"][
                metric_column_name
            ] = metric_value

    return data_columns


# Aggregations
def apply_aggregations(
    value: Any,
    column_name: str,
    columns_aggregation_config: dict,
    columns_statistics: dict,
) -> Any:
    if not columns_aggregation_config[column_name]:
        return value

    if "type" not in columns_aggregation_config[column_name]:
        print(columns_aggregation_config[column_name])
        raise ValueError(f"Aggregation type not specified for column '{column_name}'")

    aggregation_type = columns_aggregation_config[column_name]["type"]
    if aggregation_type == "evenRange":
        # Get the min and max values from the statistics
        min_value = columns_statistics[column_name]["metrics"]["min"]
        max_value = columns_statistics[column_name]["metrics"]["max"]

        # Get the nb chunks from the aggregation config
        nb_chunks = columns_aggregation_config[column_name]["nbChunks"]

        # Calculate the range size
        range_size = (max_value - min_value) / nb_chunks

        # Calculate the index of the range
        if range_size == 0:
            index = 0
        else:
            index = int((value - min_value) / range_size)
        index = max(0, index)
        index = min(index, nb_chunks - 1)

        # Return "[range_start, range_end]"
        return "[{}, {}]".format(
            round(min_value + index * range_size, 2),
            round(min_value + (index + 1) * range_size, 2),
        )
    if aggregation_type == "firstCharacters":
        # Get the number of characters from the aggregation config
        nb_characters = columns_aggregation_config[column_name]["nbCharacters"]
        nb_characters_skip = columns_aggregation_config[column_name].get(
            "nbCharactersSkip", 0
        )

        # Return the first nb_characters of the value
        return str(value)[
            nb_characters_skip : nb_characters_skip + nb_characters  # noqa: E203
        ]
    else:
        raise ValueError(
            f"Unknown aggregation type '{aggregation_type}' for column '{column_name}'"
        )
