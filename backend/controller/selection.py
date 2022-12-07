#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager

#############################################################################
# Selections Management
#############################################################################


def get_selections(projectId):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)

    return data_provider.get_selections(projectId), 200


def post_selection(projectId, data):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)

    data_provider.create_selection(
        projectId,
        data["selectionName"],
        data["sampleHashList"],
        data["requestId"] if "requestId" in data else None
    )
    return "Selection added", 200


def delete_selection(projectId, selectionId):
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    if not debiaiUtils.selectionExist(projectId, selectionId):
        return "The selection doesn't exist", 404

    debiaiUtils.deleteSelection(projectId, selectionId)

    return 200
