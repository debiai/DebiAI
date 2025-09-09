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
from debiaiServer.api.v1.debiai.utils import make_hash


def get_exploration_available_config():
    pass


def get_explorations(project_id, prev_hash_content=None):
    """
    Get all explorations with hash-based caching support.
    Returns 304 if content hasn't changed, 200 with data if it has.
    """
    explorations: List[dict] = project_explorations_db.get(project_id) or []

    # Create a clean copy for response (remove large data fields)
    clean_explorations = []
    for exploration in explorations:
        clean_exploration = exploration.copy()
        clean_exploration.pop("combinations", None)
        clean_exploration.pop("metrics", None)
        clean_explorations.append(clean_exploration)

    # Create hash from the clean explorations data
    new_hash = f"explorations_{project_id}_{str(make_hash(clean_explorations))}"

    print(
        f"Explorations hash check: {new_hash} <=> {prev_hash_content} "
        f"(types: {type(new_hash)}, {type(prev_hash_content)}) "
        f"equal: {new_hash == prev_hash_content}"
    )

    # Check if content has changed
    if new_hash == prev_hash_content:
        return None, 304
    else:
        response = {"explorations": clean_explorations, "hash_content": new_hash}
        return response, 200


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


def get_exploration(project_id, exploration_id, prev_hash_content=None):
    """
    Get a specific exploration with hash-based caching support.
    Returns 304 if content hasn't changed, 200 with data if it has.
    """
    exploration = get_exploration_by_id(project_id, exploration_id)

    if exploration is None:
        return None, 404

    # Create hash from the exploration data
    new_hash = (
        f"exploration_{project_id}_{exploration_id}_{str(make_hash(exploration))}"
    )

    print(
        f"Exploration hash check: {new_hash} <=> {prev_hash_content} "
        f"(types: {type(new_hash)}, {type(prev_hash_content)}) "
        f"equal: {new_hash == prev_hash_content}"
    )

    # Check if content has changed
    if new_hash == prev_hash_content:
        return None, 304
    else:
        response = {"exploration": exploration, "hash_content": new_hash}
        return response, 200


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
    # Get exploration directly from utils, not through the cached version
    exploration = get_exploration_by_id(project_id, exploration_id)
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
