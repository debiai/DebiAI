#############################################################################
# Imports
#############################################################################
import os

import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
import utils.hashUtils as hashUtils

dataPath = debiaiUtils.dataPath

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
@utils.traceLogLight
def get_list(projectId, data):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Get the hashmap
    hashmap = debiaiUtils.getHashmap(projectId)

    # Get params
    selectionIds = data["selectionIds"]
    selectionIntersection = data["selectionIntersection"]
    modelIds = data["modelIds"]
    commonResults = data["commonResults"]

    if not selectionIds or len(selectionIds) == 0:
        # Start form all the project samples
        samples = hashmap.keys()
    else:
        # Or from the selections samples
        try:
            samples = debiaiUtils.getSelectionsSamples(
                projectId, selectionIds, selectionIntersection)
        except KeyError as e:
            print(e)
            return "selection not found", 404

    if len(samples) == 0:
        return {
            "samples": [],
            "nbSamples": 0,
            "nbFromSelection": 0,
            "nbFromModels": 0
        }

    nbFromSelection = len(samples)
    nbFromModels = 0
    # Then, concat with the model results if given
    if modelIds and len(modelIds) > 0:
        modelSamples = debiaiUtils.getModelListResults(
            projectId, modelIds, commonResults)
        nbFromModels = len(modelSamples)
        samples = set(samples)
        samples.intersection_update(set(modelSamples))

    return {
        "samples": list(samples),
        "nbSamples": len(samples),
        "nbFromSelection": nbFromSelection,
        "nbFromModels": nbFromModels
    }, 200

# Get the list of samples ID of the project selection


@utils.traceLogLight
def get_selection_list(projectId, selectionId):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Load selection sample list
    selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

    if not selectionDetails:
        return "Selection " + selectionId + " not found", 404

    return selectionDetails["samples"], 200
