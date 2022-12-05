import os, shutil
import ujson as json

from backend.dataProviders.pythonDataProvider.dataUtils import utils, hash

DATA_PATH = utils.DATA_PATH


def getProject(projectId):
    try:
        # Json info file
        if not os.path.exists(DATA_PATH + projectId + "/info.json"):
            raise Exception('The "info.json" file is missing')

        with open(DATA_PATH + projectId + "/info.json") as json_file:
            data = json.load(json_file)

        if "name" not in data:
            raise Exception("The project name is missing from the info.json file")

        if "creationDate" not in data:
            raise Exception(
                "The project creationDate is missing from the info.json file"
            )

        if "updateDate" not in data:
            raise Exception("The project updateDate is missing from the info.json file")

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
        }

    except Exception as e:
        projectOverview = {
            "id": projectId,
            "name": projectId,
            "error": True,
            "exeption": str(e),
        }

    return projectOverview


def getProjects():
    project = []

    for projectId in os.listdir(DATA_PATH):
        project.append(getProject(projectId))

    return project


def createProject(projectId, projectName):
    # Create the project files and folders
    os.mkdir(DATA_PATH + projectId)
    os.mkdir(DATA_PATH + projectId + "/blocks")
    os.mkdir(DATA_PATH + projectId + "/models")
    os.mkdir(DATA_PATH + projectId + "/requests")
    os.mkdir(DATA_PATH + projectId + "/selections")

    now = utils.timeNow()
    projectInfo = {
        "name": projectName,
        "id": projectId,
        "creationDate": now,
        "updateDate": now,
        "blockLevelInfo": [],
    }

    utils.writeJsonFile(DATA_PATH + projectId + "/info.json", projectInfo)
    utils.writeJsonFile(DATA_PATH + projectId + "/samplesHashmap.json", {})


def updateProject(projectId):
    # Change the update date of the project to now
    utils.updateJsonFile(
        DATA_PATH + projectId + "/info.json", "updateDate", utils.timeNow()
    )


def projectExist(projectId):
    return projectId in os.listdir(DATA_PATH)


def getProjectblockLevelInfo(projectId):
    if not os.path.isfile(DATA_PATH + projectId + "/info.json"):
        raise Exception(
            "The project '" + projectId + "' doesn't have an info.json file"
        )

    with open(DATA_PATH + projectId + "/info.json") as json_file:
        return json.load(json_file)["blockLevelInfo"]


def getResultStructure(projectId):
    with open(DATA_PATH + projectId + "/info.json") as json_file:
        projectInfo = json.load(json_file)
        if "resultStructure" in projectInfo:
            return projectInfo["resultStructure"]
        else:
            return None


def deleteProject(projectId):
    # Delete the project files and folders
    try:
        shutil.rmtree(DATA_PATH + projectId)
    except Exception as e:
        print(e)
        raise "Something went wrong when deleting the project"