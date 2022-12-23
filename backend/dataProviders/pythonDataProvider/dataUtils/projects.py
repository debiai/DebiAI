import os
import shutil
import ujson as json

from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils, hash

DATA_PATH = pythonModuleUtils.DATA_PATH


def project_exist(projectId):
    return projectId in os.listdir(DATA_PATH)


def get_project(projectId):
    try:
        # Json info file
        if not os.path.exists(DATA_PATH + projectId + "/info.json"):
            raise Exception('The "info.json" file is missing')

        with open(DATA_PATH + projectId + "/info.json") as json_file:
            data = json.load(json_file)

        if "name" not in data:
            raise Exception(
                "The project name is missing from the info.json file")

        if "creationDate" not in data:
            raise Exception(
                "The project creationDate is missing from the info.json file"
            )

        if "updateDate" not in data:
            raise Exception(
                "The project updateDate is missing from the info.json file")

        name = data["name"]
        creationDate = data["creationDate"]
        updateDate = data["updateDate"]

        # Nb models
        if not os.path.exists(DATA_PATH + projectId + "/models/"):
            raise Exception('The "models" folder is missing')

        nbModels = len(os.listdir(DATA_PATH + projectId + "/models/"))

        # Nb requests
        nbRequests = 0
        if os.path.exists(DATA_PATH + projectId + "/requests/"):
            nbRequests = len(os.listdir(DATA_PATH + projectId + "/requests/"))

        # Nb selection
        if not os.path.exists(DATA_PATH + projectId + "/selections/"):
            raise Exception('The "selections" folder is missing')

        nbSelection = len(os.listdir(DATA_PATH + projectId + "/selections/"))

        # Nb samples
        if not os.path.exists(DATA_PATH + projectId + "/samplesHashmap.json"):
            raise Exception('The "samplesHashmap.json" file is missing')

        nbSamples = len(hash.getHashmap(projectId))

        # Nb tags
        nbTags = 0
        if os.path.exists(DATA_PATH + projectId + "/tags/"):
            nbTags = len(os.listdir(DATA_PATH + projectId + "/tags/"))

        projectOverview = {
            "id": projectId,
            "name": name,
            "nbModels": nbModels,
            "nbSelections": nbSelection,
            "nbRequests": nbRequests,
            "nbSamples": nbSamples,
            "nbTags": nbTags,
            "creationDate": creationDate,
            "updateDate": updateDate,
            "blockLevelInfo": get_project_block_level_info(projectId),
        }

    except Exception as e:
        projectOverview = {
            "id": projectId,
            "name": projectId,
            "error": True,
            "exeption": str(e),
        }

    return projectOverview


def get_projects():
    project = []

    for projectId in os.listdir(DATA_PATH):
        project.append(get_project(projectId))

    return project


def create_project(projectId, projectName):
    # Create the project files and folders
    os.mkdir(DATA_PATH + projectId)
    os.mkdir(DATA_PATH + projectId + "/blocks")
    os.mkdir(DATA_PATH + projectId + "/models")
    os.mkdir(DATA_PATH + projectId + "/requests")
    os.mkdir(DATA_PATH + projectId + "/selections")

    now = pythonModuleUtils.timeNow()
    projectInfo = {
        "name": projectName,
        "id": projectId,
        "creationDate": now,
        "updateDate": now,
        "blockLevelInfo": [],
    }

    pythonModuleUtils.writeJsonFile(
        DATA_PATH + projectId + "/info.json", projectInfo)
    pythonModuleUtils.writeJsonFile(
        DATA_PATH + projectId + "/samplesHashmap.json", {})

    return projectInfo


def update_project(projectId):
    # Change the update date of the project to now
    pythonModuleUtils.updateJsonFile(
        DATA_PATH + projectId + "/info.json", "updateDate", pythonModuleUtils.timeNow()
    )


def get_project_block_level_info(projectId):
    if not os.path.isfile(DATA_PATH + projectId + "/info.json"):
        raise Exception(
            "The project '" + projectId + "' doesn't have an info.json file"
        )

    with open(DATA_PATH + projectId + "/info.json") as json_file:
        return json.load(json_file)["blockLevelInfo"]


def get_result_structure(projectId):
    with open(DATA_PATH + projectId + "/info.json") as json_file:
        projectInfo = json.load(json_file)
        if "resultStructure" in projectInfo:
            return projectInfo["resultStructure"]
        else:
            return None


def delete_project(projectId):
    # Delete the project files and folders
    try:
        shutil.rmtree(DATA_PATH + projectId)
    except Exception as e:
        print(e)
        raise "Something went wrong when deleting the project"


def update_block_structure(projectId, blockStructure):
    try:
        pythonModuleUtils.updateJsonFile(
            DATA_PATH + projectId + "/info.json", "blockLevelInfo", blockStructure)

        update_project(projectId)
    except Exception as e:
        print(e)
        raise "Something went wrong updating project structure"


def update_results_structure(projectId, resultStructure):
    try:
        # save resultStructure
        pythonModuleUtils.updateJsonFile(
            DATA_PATH + projectId + "/info.json", "resultStructure", resultStructure
        )
        update_project(projectId)
        return resultStructure, 200

    except Exception as e:
        print(e)
        raise "Something went wrong updating project structure"
