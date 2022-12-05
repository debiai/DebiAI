import os
import ujson as json

from backend.dataProviders.pythonDataProvider.dataUtils import utils, samples

DATA_PATH = utils.DATA_PATH

# Selections
def createSelection(
    projectId, selectionId, selectionName, sampleHashList, requestId=None
):
    selectionInfoFilePath = (
        DATA_PATH + projectId + "/selections/" + selectionId + "/info.json"
    )

    now = utils.timeNow()

    selectionInfo = {
        "id": selectionId,
        "name": selectionName,
        "filePath": selectionInfoFilePath,
        "creationDate": now,
        "updateDate": now,
        "samples": sampleHashList,
    }

    if requestId is not None:
        selectionInfo["requestId"] = requestId

    os.mkdir(DATA_PATH + projectId + "/selections/" + selectionId)
    utils.writeJsonFile(selectionInfoFilePath, selectionInfo)
    updateProject(projectId)
    return selectionInfo


def getSelectionIds(projectId):
    return os.listdir(DATA_PATH + projectId + "/selections/")


def selectionExist(projectId, selectionId):
    return selectionId in getSelectionIds(projectId)


def getSelectionInfo(projectId, selectionId):
    with open(
        DATA_PATH + projectId + "/selections/" + selectionId + "/info.json"
    ) as json_file:
        data = json.load(json_file)
        ret = {
            "id": data["id"],
            "name": data["name"],
            "filePath": data["filePath"],
            "creationDate": data["creationDate"],
            "updateDate": data["updateDate"],
            "nbSamples": len(data["samples"]),
        }

        # Add the request Id if it exist
        if "requestId" in data:
            ret["requestId"] = data["requestId"]

        return ret


def getSelection(projectId, selectionId):
    # Same as getSelectionInfo but with the samples
    # TODO : set the samples as a csv file
    if not selectionExist(projectId, selectionId):
        return None

    with open(
        DATA_PATH + projectId + "/selections/" + selectionId + "/info.json"
    ) as json_file:
        data = json.load(json_file)
        ret = {
            "id": data["id"],
            "name": data["name"],
            "filePath": data["filePath"],
            "creationDate": data["creationDate"],
            "updateDate": data["updateDate"],
            "nbSamples": len(data["samples"]),
            "samples": data["samples"],
        }

        # Add the request Id if it exist
        if "requestId" in data:
            ret["requestId"] = data["requestId"]
        return ret


def getSelectionSamples(projectId, selectionId):
    selectionData = getSelection(projectId, selectionId)
    if not selectionData:
        raise KeyError("Selection " + selectionId + " doesn't exist")

    if "samples" not in selectionData:
        return []
    return selectionData["samples"]


def getSelectionsSamples(projectId, selectionIds: list, intersection: bool) -> set:
    if len(selectionIds) == 0:
        return []

    samples = set(getSelectionSamples(projectId, selectionIds[0]))
    for selectionId in selectionIds[1:]:
        if intersection:  # intersection of the selections samples
            samples.intersection_update(getSelectionSamples(projectId, selectionId))

            if len(samples) == 0:
                return []
        else:  # Union of the model results samples
            samples = samples.union(getSelectionSamples(projectId, selectionId))

    return samples


def deleteSelection(projectId, selectionId):
    utils.deleteDir(DATA_PATH + projectId + "/selections/" + selectionId)
    updateProject(projectId)
