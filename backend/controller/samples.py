#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
def get_list(projectId, data):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    
    if "from" in data and "to" in data:
        from_index = int(data["from"])
        to_index = int(data["to"])
        data_id_list = data_provider.get_id_list(projectId, from_index, to_index)
    else :
        data_id_list = data_provider.get_id_list(projectId)

    return {"samples": data_id_list}, 200

# Get the list of samples ID of the project selection
def get_selection_list(projectId, selectionId):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Load selection sample list
    selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

    if not selectionDetails:
        return "Selection " + selectionId + " not found", 404

    return selectionDetails["samples"], 200
