import uuid
import threading
from typing import List
from .utils import (
    explorations_db,
    start_exploration_real_combination_computation,
    create_selection,
    update_exploration_db,
    computation_threads,
    stop_flags,
)
from debiaiServer.api.v1.debiai.utils import make_hash


def get_exploration_available_config():
    pass


def get_explorations(project_id, prev_hash_content=None):
    explorations: List[dict] = []
    for exploration_id in explorations_db.all():
        exploration = explorations_db.get(exploration_id)
        if exploration.get("project_id") != project_id:
            continue

        exploration.pop("combinations", None)
        exploration.pop("metrics", None)
        explorations.append(exploration)

    new_hash = "exploration_" + str(make_hash(explorations))

    if new_hash == prev_hash_content:
        return None, 304
    else:
        explorations_answer = {
            "explorations": explorations,
            "hash_content": new_hash,
        }
        return explorations_answer, 200


def create_exploration(project_id, body):
    # Get current explorations
    exploration_id = str(uuid.uuid4())
    new_exploration = {
        "id": exploration_id,
        "project_id": project_id,
        "name": body.get("name"),
        "description": body.get("description", ""),
        "state": "not_started",
        "config": {},
    }

    # Add new exploration
    explorations_db.set(exploration_id, new_exploration)
    explorations_db.save()
    return 201


def get_exploration(exploration_id):
    exploration = explorations_db.get(exploration_id)
    if exploration:
        return exploration, 200
    else:
        return 404


def delete_exploration(exploration_id):
    explorations_db.remove(exploration_id)
    return 204


def update_exploration(exploration_id, action, body):
    exploration = explorations_db.get(exploration_id)
    if exploration is None:
        print("Exploration not found:", exploration_id)
        return None, 404

    # Perform action based on the request
    if action == "start":
        # Check if the exploration is already running
        if exploration.get("state") == "ongoing":
            print("Exploration is already running:", exploration_id)
            return exploration

        # Start the exploration computation in a separate thread
        print(exploration_id)
        thread = threading.Thread(
            target=start_exploration_real_combination_computation,
            args=(exploration_id,),
            daemon=True,
        )
        thread.start()

        exploration["state"] = "ongoing"
        # Save the thread in the global dictionary
        computation_threads[exploration_id] = thread
        update_exploration_db(exploration_id, exploration)

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

        update_exploration_db(exploration_id, exploration)
        return exploration
    elif action == "updateConfig":
        # Do not update the exploration if it is running
        if exploration.get("state") == "ongoing":
            print("Cannot update config while exploration is running:", exploration_id)
            return exploration

        # Update exploration config
        exploration["config"] = body
        update_exploration_db(exploration_id, exploration)
        return exploration
    else:
        raise ValueError(f"Unknown action: {action}")


def update_exploration_config():
    pass


def create_exploration_selection(exploration_id, body):
    exploration = explorations_db.get(exploration_id)
    # Create a selection for the exploration
    create_selection(
        exploration.get("project_id"),
        exploration_id,
        body["selected_combinations"],
        body["selection_name"],
    )

    return 201
