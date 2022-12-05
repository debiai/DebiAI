#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.pythonDataProvider.PythonDataProvider as PythonDataProvider

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
def get_list(projectId, data):
    print(projectId)
    print("get_list")
    print(data)
    if "from" in data:
        print(data["from"])
    if "to" in data:
        print(data["to"])

    if debiaiUtils.projectExist(projectId):
        return samplesUtils.get_list(projectId, data), 200

    if dataProviders.projectExist(projectId):
        return dataProviders.get_list(projectId, data), 200

    return "project not found", 404


# Get the list of samples ID of the project selection
def get_selection_list(projectId, selectionId):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Load selection sample list
    selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

    if not selectionDetails:
        return "Selection " + selectionId + " not found", 404

    return selectionDetails["samples"], 200
