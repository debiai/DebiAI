from pickledb import PickleDB
import uuid

# Create or load a database
project_explorations_db = PickleDB("projectsExplorationsStatistics.db")


def get_columns_statistics(dataProviderId, projectId):
    return {"columns": [], "status": "ongoing"}
