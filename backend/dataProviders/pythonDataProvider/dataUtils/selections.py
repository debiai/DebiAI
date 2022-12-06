import os
import ujson as json

from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils, projects
DATA_PATH = pythonModuleUtils.DATA_PATH

# Selections


def create_selection(
    projectId, selectionId, selectionName, sampleHashList, requestId=None
):
    selectionInfoFilePath = (
        DATA_PATH + projectId + "/selections/" + selectionId + "/info.json"
    )

    now = pythonModuleUtils.timeNow()

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
    pythonModuleUtils.writeJsonFile(selectionInfoFilePath, selectionInfo)
    projects.updateProject(projectId)
    projects.updateProject(projectId)
    return selectionInfo


def get_selections(projectId):
    # Get selections
    selections = []
    for selectionId in get_selection_ids(projectId):
        selections.append(get_selection(projectId, selectionId))
    return selections


def get_selection_ids(projectId):
    return os.listdir(DATA_PATH + projectId + "/selections/")


def selection_exist(projectId, selectionId):
    return os.path.exists(DATA_PATH + projectId + "/selections/" + selectionId)


def get_selection(projectId, selectionId):
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


def get_selection_id_list(projectId, selectionId):
    if not selection_exist(projectId, selectionId):
        raise Exception("Selection " + selectionId + " doesn't exist")

    with open(
        DATA_PATH + projectId + "/selections/" + selectionId + "/info.json"
    ) as json_file:
        data = json.load(json_file)
        return data["samples"]


# def getSelectionsSamples(projectId, selectionIds: list, intersection: bool) -> set:
#     if len(selectionIds) == 0:
#         return []

#     samples = set(get_selection_id_list(projectId, selectionIds[0]))
#     for selectionId in selectionIds[1:]:
#         if intersection:  # intersection of the selections samples
#             samples.intersection_update(
#                 get_selection_id_list(projectId, selectionId))

#             if len(samples) == 0:
#                 return []
#         else:  # Union of the model results samples
#             samples = samples.union(
#                 get_selection_id_list(projectId, selectionId))

#     return samples


def deleteSelection(projectId, selectionId):
    pythonModuleUtils.deleteDir(
        DATA_PATH + projectId + "/selections/" + selectionId)
    projects.updateProject(projectId)
