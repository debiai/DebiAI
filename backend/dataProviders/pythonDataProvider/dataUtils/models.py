import os
import ujson as json
from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils, selections, projects

DATA_PATH = pythonModuleUtils.DATA_PATH


#  Models
def get_model_ids(projectId):
    return os.listdir(DATA_PATH + projectId + "/models/")


def get_models(projectId):
    ret = []
    for model in os.listdir(DATA_PATH + projectId + "/models/"):
        with open(DATA_PATH + projectId + "/models/" + model + "/info.json") as json_file:
            info = json.load(json_file)
            ret.append(
                {
                    "name": model,
                    "id": model,
                    "creationDate": info["creationDate"],
                    "updateDate": info["updateDate"],
                    "version": "0.0.0",
                    "metaDataList": info["metadata"],
                    "nbResults": info["nbResults"],
                }
            )

    return ret

def model_exist(projectId, modelId):
    return modelId in get_model_ids(projectId)


def delete_model(projectId, modelId):
    pythonModuleUtils.deleteDir(DATA_PATH + projectId + "/models/" + modelId)


def write_model_results(projectId, modelId, results):
    pythonModuleUtils.writeJsonFile(
        DATA_PATH + projectId + "/models/" + modelId + "/results.json", results
    )
    projects.updateProject(projectId)


def get_model_results(projectId, modelId, selectionId=None):
    # Get the models results from the project or a selection
    with open(
        DATA_PATH + projectId + "/models/" + modelId + "/results.json", "r"
    ) as jsonFile:
        d = json.load(jsonFile)

    if not selectionId:
        return d
    else:
        selectionSamples = set(selections.getSelectionSamples(projectId, selectionId))
        return selectionSamples.intersection_update(d)


def get_model_list_results(projectId, modelIds: list, common: bool) -> list:
    samples = set(get_model_results(projectId, modelIds[0]))

    for modelId in modelIds[1:]:
        if common:  # Common samples between models
            samples.intersection_update(get_model_results(projectId, modelId))
        else:  # Union of the model results samples
            samples = samples.union(get_model_results(projectId, modelId))

    return list(samples)
