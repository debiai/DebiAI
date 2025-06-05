from pickledb import PickleDB
import uuid

# Create or load a database
project_explorations_db = PickleDB("projectsExplorations.db")


def get_exploration_available_config():
    pass


def get_explorations(project_id):
    return project_explorations_db.get(project_id) or []


def create_exploration(project_id, body):
    # Get current explorations
    explorations = project_explorations_db.get(project_id) or []

    # Add new exploration
    explorations.append(
        {
            "id": str(uuid.uuid4()),
            "name": body.get("name"),
            "description": body.get("description", ""),
            "config": {},
        }
    )

    # Update the database
    project_explorations_db.set(project_id, explorations)
    project_explorations_db.save()


def get_exploration(project_id, exploration_id):
    explorations = project_explorations_db.get(project_id) or []
    for exploration in explorations:
        if exploration.get("id") == exploration_id:
            return exploration
    return None


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
    project_explorations_db.set(project_id, explorations)
    project_explorations_db.save()
    return explorations


def update_exploration(project_id, exploration_id, action, body):
    exploration = get_exploration(project_id, exploration_id)
    if exploration is None:
        return None

    # Perform action based on the request
    if action == "start":
        return
    elif action == "stop":
        return
    elif action == "updateConfig":
        # Update exploration config
        exploration["config"] = body
        print("Updated exploration config:", exploration["config"])
        project_explorations_db.set(project_id, project_explorations_db.get(project_id))
        project_explorations_db.save()
        return exploration
    else:
        raise ValueError(f"Unknown action: {action}")


def update_exploration_config():
    pass
