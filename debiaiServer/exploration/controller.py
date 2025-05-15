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
        }
    )

    # Update the database
    project_explorations_db.set(project_id, explorations)


def get_exploration_config(project_id, exploration_id):
    explorations = project_explorations_db.get(project_id) or []
    for exploration in explorations:
        if exploration.get("id") == exploration_id:
            return exploration
    return None


def delete_exploration():
    pass


def update_exploration():
    pass


def update_exploration_config():
    pass
