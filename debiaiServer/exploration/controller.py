import uuid
import threading
from typing import List
from .utils import (
    project_explorations_db,
    start_exploration_real_combination_computation,
    get_exploration_by_id,
    update_explorations,
    update_exploration as update_exploration_db,
    create_selection,
    computation_threads,
    stop_flags,
)


def get_exploration_available_config():
    pass


def get_explorations(project_id):
    explorations: List[dict] = project_explorations_db.get(project_id) or []
    for exploration in explorations:
        exploration.pop("combinations", None)
        exploration.pop("metrics", None)
    return explorations


def create_exploration(project_id, body):
    # Get current explorations
    explorations = project_explorations_db.get(project_id) or []

    # Add new exploration
    explorations.append(
        {
            "id": str(uuid.uuid4()),
            "name": body.get("name"),
            "description": body.get("description", ""),
            "state": "not_started",
            "config": {},
        }
    )

    # Update the database
    update_explorations(project_id, explorations)


def get_exploration(project_id, exploration_id):
    return get_exploration_by_id(project_id, exploration_id)


def delete_exploration(project_id, exploration_id):
    # Get current explorations
    explorations = project_explorations_db.get(project_id) or []

    # Filter out the exploration to delete
    explorations = [
        exploration
        for exploration in explorations
        if exploration.get("id") != exploration_id
    ]

    # Update the database
    update_explorations(project_id, explorations)
    return explorations


def update_exploration(project_id, exploration_id, action, body):
    exploration = get_exploration(project_id, exploration_id)
    if exploration is None:
        print("Exploration not found:", exploration_id)
        return None

    # Perform action based on the request
    if action == "start":
        # Check if the exploration is already running
        if exploration.get("state") == "ongoing":
            print("Exploration is already running:", exploration_id)
            return exploration

        # Start the exploration computation in a separate thread
        thread = threading.Thread(
            target=start_exploration_real_combination_computation,
            args=(project_id, exploration_id),
            daemon=True,
        )
        thread.start()

        # Save the thread in the global dictionary
        computation_threads[exploration_id] = thread

        return exploration
    elif action == "stop":
        # Stop the exploration computation
        if exploration_id in computation_threads:
            # Set the stop flag
            stop_flags[exploration_id] = True

            # Wait for the thread to finish
            computation_threads[exploration_id].join()
            del computation_threads[exploration_id]
            del stop_flags[exploration_id]
        elif exploration.get("state") == "ongoing":
            # Exploration is ongoing but no thread found, set state to not_started
            exploration["state"] = "not_started"

        return exploration
    elif action == "updateConfig":
        # Do not update the exploration if it is running
        if exploration.get("state") == "ongoing":
            print("Cannot update config while exploration is running:", exploration_id)
            return exploration

        # Update exploration config
        exploration["config"] = body
        update_exploration_db(project_id, exploration)
        return exploration
    else:
        raise ValueError(f"Unknown action: {action}")


def update_exploration_config():
    pass


def create_exploration_selection(project_id, exploration_id, body):
    # Create a selection for the exploration
    create_selection(
        project_id,
        exploration_id,
        body["selected_combinations"],
        body["selection_name"],
    )

    return 201
