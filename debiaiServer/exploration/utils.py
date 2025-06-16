from pickledb import PickleDB
from ..exploration_statistics.utils import get_data_batch
from ..modules.dataProviders.dataProviderManager import (
    get_single_data_provider_for_project_id,
)
from uuid import uuid4
from time import time
import traceback
from collections import defaultdict

# Create or load a database
project_explorations_db = PickleDB("projectsExplorations.db")
computation_threads = {}
stop_flags = {}


# DB operations
def get_exploration_by_id(project_id, exploration_id):
    explorations = project_explorations_db.get(project_id) or []
    for exploration in explorations:
        if exploration.get("id") == exploration_id:
            return exploration
    return None


def update_explorations(project_id, explorations):
    project_explorations_db.set(project_id, explorations)
    project_explorations_db.save()


def update_exploration(project_id, exploration):
    explorations = project_explorations_db.get(project_id) or []
    for i, existing_exploration in enumerate(explorations):
        if existing_exploration.get("id") == exploration.get("id"):
            explorations[i] = exploration
            break
    else:
        explorations.append(exploration)

    update_explorations(project_id, explorations)
    return exploration


# Processing functions
def start_exploration_real_combination_computation(project_id, exploration_id):
    try:
        _start_exploration_real_combination_computation(project_id, exploration_id)
    except Exception as e:
        print(f"Error during exploration computation: {e}")
        traceback.print_exc()
        exploration = get_exploration_by_id(project_id, exploration_id)
        if exploration:
            exploration["state"] = "error"
            update_exploration(project_id, exploration)
        return


def _start_exploration_real_combination_computation(project_id, exploration_id):
    # Get the exploration from the database
    exploration = get_exploration_by_id(project_id, exploration_id)
    if exploration is None:
        return
    selected_columns = exploration.get("config", {}).get("selectedColumns", [])
    if not selected_columns:
        print(
            f"No selected columns for exploration {exploration_id} on project {project_id}"
        )
        return

    # Get the data-provider for the given project
    data_provider = get_single_data_provider_for_project_id(project_id)
    print(f"Starting exploration {exploration_id} on project {project_id}")
    print(f"Using data provider: {data_provider.name}")
    columns_structure = data_provider.get_project(project_id)["columns"]

    # Set the exploration as started
    exploration["state"] = "ongoing"
    exploration["real_combinations"] = 0
    exploration["started_at"] = time()
    exploration["current_sample"] = 0
    exploration["remaining_time"] = None
    update_exploration(project_id, exploration)

    # Combinations computation
    combinations = defaultdict(list)
    NB_SAMPLES = 1000
    current_sample = 0
    computation_id = str(uuid4())
    while True:
        # Check if the stop signal is set, stop the exploration if it is
        if stop_flags.get(exploration_id):
            print(f"Stopping exploration {exploration_id}")
            exploration["state"] = "not_started"
            update_exploration(project_id, exploration)
            return

        # Fetch the next batch of samples
        batch = get_data_batch(
            data_provider,
            project_id,
            computation_id,
            current_sample,
            current_sample + NB_SAMPLES,
            columns_structure,
            selected_columns,
        )

        for data_id, values in batch.items():
            combinations[tuple(values)].append(data_id)

        # Update the exploration progression status
        current_sample += len(batch)
        exploration["current_sample"] = current_sample
        exploration["real_combinations"] = len(combinations.keys())

        # Calculate the estimated time remaining
        elapsed_time = time() - exploration["started_at"]
        if exploration["current_sample"] > 0:
            estimated_total_time = (
                elapsed_time * NB_SAMPLES / exploration["current_sample"]
            )
            exploration["remaining_time"] = estimated_total_time - elapsed_time

        # Update the exploration in the database
        update_exploration(project_id, exploration)

        # If the batch is less than the requested size, we assume we reached the end
        if len(batch) < NB_SAMPLES:
            print("Reached the end of the data provider samples.")
            break

        print(f"Time: {time() - exploration['started_at']:.2f}s, ")

    # Convert combinations to JSON format
    combinations_json = []
    for key, value in combinations.items():
        combinations_json.append({"sample_ids": value, "combination": list(key)})

    # Set the exploration status to "completed"
    exploration["combinations"] = combinations_json
    exploration["state"] = "completed"
    exploration["finished_at"] = time()

    update_exploration(project_id, exploration)
