import os
import ujson as json

from backend.dataProviders.pythonDataProvider.dataUtils import utils, projects

DATA_PATH = utils.DATA_PATH

#  Models
def getModelIds(projectId):
    return os.listdir(DATA_PATH + projectId + "/models/")


def getModelInfo(projectId, modelId):
    with open(DATA_PATH + projectId + "/models/" + modelId + "/info.json") as json_file:
        return json.load(json_file)


def modelExist(projectId, modelId):
    return modelId in getModelIds(projectId)


def getModelsId(projectId):
    return os.listdir(DATA_PATH + projectId + "/models/")


def deleteModel(projectId, modelId):
    utils.deleteDir(DATA_PATH + projectId + "/models/" + modelId)


def writeModelResults(projectId, modelId, results):
    utils.writeJsonFile(
        DATA_PATH + projectId + "/models/" + modelId + "/results.json", results
    )
    projects.updateProject(projectId)


def getModelResults(projectId, modelId, selectionId=None):
    # Get the models results from the project or a selection
    with open(
        DATA_PATH + projectId + "/models/" + modelId + "/results.json", "r"
    ) as jsonFile:
        d = json.load(jsonFile)

    if not selectionId:
        return d
    else:
        selectionSamples = set(getSelectionSamples(projectId, selectionId))
        return selectionSamples.intersection_update(d)


def getModelListResults(projectId, modelIds: list, common: bool) -> list:
    samples = set(getModelResults(projectId, modelIds[0]))

    for modelId in modelIds[1:]:
        if common:  # Common samples between models
            samples.intersection_update(getModelResults(projectId, modelId))
        else:  # Union of the model results samples
            samples = samples.union(getModelResults(projectId, modelId))

    return list(samples)
