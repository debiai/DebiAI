from pickledb import PickleDB
from ..exploration_statistics.utils import get_data_batch, get_columns_statistics
from debiaiServer.modules.dataProviders.dataProviderManager import (
    get_single_data_provider_for_project_id,
)
from uuid import uuid4
from time import time
import traceback
from collections import defaultdict

# Create or load a database
explorations_db = PickleDB("Explorations.db")
computation_threads = {}
stop_flags = {}


# DB operations


def update_exploration_db(exploration_id, exploration):
    explorations_db.set(exploration_id, exploration)
    explorations_db.save()


# Processing functions
def start_exploration_real_combination_computation(exploration_id):
    try:
        _start_exploration_real_combination_computation(exploration_id)
    except Exception as e:
        print(f"Error during exploration computation: {e}")
        traceback.print_exc()
        exploration = explorations_db.get(exploration_id)
        if exploration:
            exploration["state"] = "error"
            update_exploration_db(exploration_id, exploration)
        return


def _start_exploration_real_combination_computation(exploration_id):
    # Get the exploration from the database
    exploration = explorations_db.get(exploration_id)
    project_id = exploration["project_id"]
    if exploration is None:
        raise ValueError(f"Exploration with ID {exploration_id} not found")
    selected_columns = exploration.get("config", {}).get("columns", [])
    if not selected_columns:
        raise ValueError(
            "No selected columns for exploration. Please select columns to explore."
        )
    selected_columns_labels = [col["label"] for col in selected_columns]
    selected_columns_aggregations = {
        col["label"]: col.get("aggregation", "none") for col in selected_columns
    }

    # Get the data-provider for the given project
    data_provider = get_single_data_provider_for_project_id(project_id)
    data_provider_info = data_provider.get_info()
    project = data_provider.get_project(project_id)
    columns_structure = project["columns"]
    project_nb_samples = project.get("nbSamples", None)

    # Set the exploration as started
    exploration["state"] = "ongoing"
    exploration["real_combinations"] = 0
    exploration["started_at"] = time()
    exploration["current_sample"] = 0
    exploration["remaining_time"] = None
    update_exploration_db(exploration_id, exploration)

    # Load the columns statistics
    columns_statistics = get_columns_statistics(data_provider.name, project_id)[
        "columns"
    ]
    columns_statistics_dict = {col["name"]: col for col in columns_statistics}

    # Set the metrics up
    metrics_values = {"Nb Samples": {"values": []}}
    metric_columns_to_fetch = set()
    for selectedSampleMetric in exploration.get("config", {}).get(
        "selectedSampleMetrics", []
    ):
        metrics_values[selectedSampleMetric] = {"values": []}
    for selectedColumnWithMetrics in exploration.get("config", {}).get(
        "column_metrics", []
    ):
        for selectedColumnMetric in selectedColumnWithMetrics.get("metrics", []):
            metric_name = (
                selectedColumnWithMetrics["columnLabel"] + "_" + selectedColumnMetric
            )
            metrics_values[metric_name] = {
                "values": [],
                "metric": selectedColumnMetric,
                "column": selectedColumnWithMetrics["columnLabel"],
            }
            metric_columns_to_fetch.add(selectedColumnWithMetrics["columnLabel"])
    metric_columns_to_fetch = list(metric_columns_to_fetch)

    # Determine the number of samples to fetch in each batch
    NB_SAMPLES = 25000
    if data_provider_info.get("maxSampleIdByRequest") and data_provider_info.get(
        "maxSampleDataByRequest"
    ):
        NB_SAMPLES = min(
            data_provider_info["maxSampleIdByRequest"],
            data_provider_info["maxSampleDataByRequest"],
        )

    # Combinations computation
    combinations = defaultdict(list)
    current_sample = 0
    computation_id = str(uuid4())
    while True:
        # Check if the stop signal is set, stop the exploration if it is
        if stop_flags.get(exploration_id):
            print(f"Stopping exploration {exploration_id}")
            exploration["state"] = "not_started"
            update_exploration_db(exploration_id, exploration)
            return

        # Fetch the next batch of samples
        batch = get_data_batch(
            data_provider,
            project_id,
            {"id": computation_id},
            current_sample,
            current_sample + NB_SAMPLES - 1,
            columns_structure,
            selected_columns_labels,
            selected_columns_aggregations,
            columns_statistics_dict,
            metric_columns_to_fetch,
        )

        # Update the combinations
        for data_id, values in batch.items():
            combinations[values["column_values"]].append(data_id)

        # Process the metrics for the current batch
        process_combination_metrics(
            current_combinations=combinations,
            data_and_metrics_batch=batch,
            metrics=metrics_values,
        )

        # Update the exploration progression status
        current_sample += len(batch)
        exploration["current_sample"] = current_sample
        exploration["real_combinations"] = len(combinations.keys())

        # Calculate the estimated time remaining
        elapsed_time = time() - exploration["started_at"]
        if exploration["current_sample"] > 0 and project_nb_samples is not None:
            estimated_total_time = (
                elapsed_time * project_nb_samples / exploration["current_sample"]
            )
            exploration["remaining_time"] = max(0, estimated_total_time - elapsed_time)

        # Update the exploration in the database
        update_exploration_db(exploration_id, exploration)

        # If the batch is less than the requested size, we assume we reached the end
        if len(batch) < NB_SAMPLES:
            print("Reached the end of the data provider samples.")
            break

    # Convert combinations to JSON format
    combinations_json = []
    for key, value in combinations.items():
        combinations_json.append({"sample_ids": value, "combination": list(key)})

    # Clean the metrics values
    for metric_name, metric_data in metrics_values.items():
        keys = list(metric_data.keys())
        for key in keys:
            if key != "values":
                del metric_data[key]

    # Set the exploration status to "completed"
    exploration["combinations"] = combinations_json
    exploration["metrics"] = metrics_values
    exploration["state"] = "completed"
    exploration["finished_at"] = time()

    update_exploration_db(exploration_id, exploration)


def process_combination_metrics(current_combinations, data_and_metrics_batch, metrics):
    """
    current_combinations:
    {
        (value1, value2): [sample_id1, sample_id2],
        (value3, value4): [sample_id3]
    }

    data_and_metrics_batch:
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

    metrics:
    {
        "Nb Samples": {
            "values": [...],
        },
        "metric1": {
            "values": [...],
            "column": "column1",
            "metric": "mean",
            ...
        },
        ...
    """

    if "Nb Samples" in metrics:
        # For each combination, count the number of samples
        metrics["Nb Samples"]["values"] = []
        for combination in current_combinations:
            metrics["Nb Samples"]["values"].append(
                len(current_combinations[combination])
            )

    for metric_name, metric_data in metrics.items():
        column_name = metric_data.get("column")
        if metric_data.get("metric") == "mean":
            # Process mean metrics
            if "combinations" not in metric_data:
                metric_data["combinations"] = {}

            for new_data in data_and_metrics_batch.values():
                if new_data["column_values"] not in metric_data["combinations"]:
                    metric_data["combinations"][new_data["column_values"]] = {
                        "mean": 0,
                        "count": 0,
                    }

                current_mean = metric_data["combinations"][new_data["column_values"]][
                    "mean"
                ]
                metric_data["combinations"][new_data["column_values"]]["count"] += 1
                current_count = metric_data["combinations"][new_data["column_values"]][
                    "count"
                ]

                metric_data["combinations"][new_data["column_values"]]["mean"] += (
                    new_data["metric_column_values"].get(column_name, 0) - current_mean
                ) / (current_count)

            # Save the mean for each combination
            metric_data["values"] = []
            for combination in current_combinations:
                if combination in metric_data["combinations"]:
                    mean_value = metric_data["combinations"][combination].get("mean", 0)
                    metric_data["values"].append(mean_value)
                else:
                    metric_data["values"].append(0)


# Selections
def create_selection(
    project_id, exploration_id, selected_combinations_id, selection_name
):
    exploration = explorations_db.get(exploration_id)

    if exploration is None:
        raise ValueError(
            f"Exploration with ID {exploration_id} not found in project {project_id}"
        )

    # Get the data provider for the project
    data_provider = get_single_data_provider_for_project_id(project_id)
    if data_provider is None:
        raise ValueError(f"No data provider found for project {project_id}")

    # Extract the selected combinations from the exploration
    combinations = exploration.get("combinations", [])
    if not combinations:
        raise ValueError(
            f"No combinations found in exploration \
{exploration_id} for project {project_id}"
        )

    # Filter the combinations based on the selected IDs
    selected_combinations = [
        comb for comb in combinations if comb["combination"] in selected_combinations_id
    ]

    # Aggregate the sample IDs from the selected combinations
    selected_sample_ids = []
    for comb in selected_combinations:
        selected_sample_ids.extend(comb["sample_ids"])

    # Create the selection
    data_provider.create_selection(
        project_id,
        selection_name,
        selected_sample_ids,
    )
