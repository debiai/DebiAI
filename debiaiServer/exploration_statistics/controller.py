from pickledb import PickleDB
import uuid
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager

# Create or load a database
project_explorations_db = PickleDB("projectsExplorationsStatistics.db")


def canCalculate(column):
    # Check if the column can be calculated
    # Only columns that have numbers or text can be calculated
    if column["hasNumbers"] and not (
        column["hasText"]
        or column["hasOther"]
        or column["hasList"]
        or column["hasDict"]
    ):
        return True
    return False


def get_columns_statistics(dataProviderId, projectId):
    SAMPLES_PER_PAGE = 500

    print(f" - Getting columns statistics for project {projectId} on {dataProviderId}")

    # Find the data provider
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    # Get the project columns structure
    print(" - Getting columns structure")
    columns_structure = data_provider.get_project(projectId)["columns"]
    print(columns_structure)
    # [
    #     {"name": "image", "category": "other", "type": "auto"},
    #     {"name": "objects", "category": "groundtruth", "type": "list"},
    #     {"name": "camera", "category": "context", "type": "text"},
    #     {"name": "objects number", "category": "context", "type": "number"},
    #     {"name": "per classes number", "category": "context", "type": "number"},
    # ]

    # Set the columns statistics
    columns_statistics = []
    for column in columns_structure:
        # Get the column statistics
        column_statistics = {
            "name": column["name"],
            "category": column["category"],
            "type": column["type"],
            "nbUniqueValues": 0,
            "average": None,
            "min": None,
            "max": None,
            "nbNullValues": 0,
            "hasNumbers": False,
            "hasText": False,
            "hasNull": False,
            "hasList": False,
            "hasDict": False,
            "hasOther": False,
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
                    column["nbNullValues"] += 1
                    column["hasNull"] = True
                    continue

                # Check the sample type
                if isinstance(sample, (int, float)):
                    column["hasNumbers"] = True
                elif isinstance(sample, str):
                    column["hasText"] = True
                elif isinstance(sample, list):
                    column["hasList"] = True
                elif isinstance(sample, dict):
                    column["hasDict"] = True
                else:
                    print("Unknown type", type(sample))
                    column["hasOther"] = True

                # Deal with the unique values
                if column["hasNumbers"] or column["hasText"]:
                    if column["name"] not in unique_values_map:
                        unique_values_map[column["name"]] = set()
                    unique_values_map[column["name"]].add(sample)

                # Update the min, max and average
                if canCalculate(column):
                    # Update the min, max and average
                    if column["min"] is None or sample < column["min"]:
                        column["min"] = sample
                    if column["max"] is None or sample > column["max"]:
                        column["max"] = sample
                    if column["average"] is None:
                        column["average"] = sample
                    else:
                        column["average"] = (
                            column["average"] * (current_sample_nb - 1) + sample
                        ) / current_sample_nb

        # If no more samples, break the loop
        nb_samples += len(data_id_list)
        print("  - nb_samples", nb_samples)
        if len(data_id_list) < SAMPLES_PER_PAGE:
            break

    # Add the nb unique values to the column statistics
    for column in columns_statistics:
        # Skip the columns that are not of type number or text
        if column["hasDict"] or column["hasList"] or column["hasOther"]:
            continue

        # Get the unique values
        if column["name"] in unique_values_map:
            column["nbUniqueValues"] = len(unique_values_map[column["name"]])

    return {"columns": columns_statistics}, 200
