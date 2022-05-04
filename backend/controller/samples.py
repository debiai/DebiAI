#############################################################################
# Imports
#############################################################################

import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
import utils.debiai.samples as samplesUtils
import utils.dataProviders as dataProviders

dataPath = debiaiUtils.dataPath

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
@utils.traceLogLight
def get_list(projectId, data):
    if debiaiUtils.projectExist(projectId):
        return samplesUtils.get_list(projectId, data), 200

    if dataProviders.projectExist(projectId):
        return dataProviders.get_list(projectId, data), 200

    return "project not found", 404


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
