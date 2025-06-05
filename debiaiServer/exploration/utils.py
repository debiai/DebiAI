from pickledb import PickleDB
from ..exploration_statistics.controller import get_samples_batch
from ..modules.dataProviders.dataProviderManager import (
    get_single_data_provider_for_project_id,
)

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
    from time import sleep, time
    from random import randint

    # Get the exploration from the database
    exploration = get_exploration_by_id(project_id, exploration_id)
    if exploration is None:
        return

    # Get the data-provider for the given project
    data_provider = get_single_data_provider_for_project_id(project_id)
    print(f"Starting exploration {exploration_id} on project {project_id}")
    print(f"Using data provider: {data_provider.name}")

    batch = get_samples_batch(
        data_provider,
        project_id,
        "aa",
        0,
        10,  # Assuming we want to start with the first 1000 samples
    )
    print(f"Fetched {len(batch)} samples from the data provider")
    print(batch)

    # Set the exploration as started
    exploration["state"] = "ongoing"
    exploration["real_combinations"] = 0
    exploration["started_at"] = time()
    exploration["current_sample"] = 0
    exploration["remaining_time"] = None
    update_exploration(project_id, exploration)

    # Combinations computation

    nb_iter = 15
    for i in range(nb_iter):
        # Check if the stop signal is set
        if stop_flags.get(exploration_id):
            print(f"Stopping exploration {exploration_id}")
            exploration["state"] = "not_started"
            update_exploration(project_id, exploration)
            return

        exploration["current_sample"] = i * 10 + 1
        exploration["real_combinations"] += randint(1, 50)

        # Calculate the estimated time remaining
        elapsed_time = time() - exploration["started_at"]
        estimated_total_time = elapsed_time / (i + 1) * nb_iter
        exploration["remaining_time"] = estimated_total_time - elapsed_time

        # Update the exploration in the database
        print(
            f"Iteration {i + 1}/{nb_iter}, "
            f"Current Sample: {exploration['current_sample']}, "
            f"Real Combinations: {exploration['real_combinations']}, "
            f"Estimated Remaining Time: {exploration['remaining_time']:.2f} seconds"
        )
        update_exploration(project_id, exploration)
        sleep(20 / nb_iter)

    # Set the exploration status to "completed"
    exploration["state"] = "completed"
    update_exploration(project_id, exploration)
