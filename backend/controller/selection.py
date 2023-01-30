#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.DataProviderException as DataProviderException

#############################################################################
# Selections Management
#############################################################################


def get_selections(projectId):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.get_selections(projectId), 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_selection(projectId, data):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.create_selection(
            projectId,
            data["selectionName"],
            data["sampleHashList"],
            data["requestId"] if "requestId" in data else None,
        )
        return "Selection added", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def delete_selection(projectId, selectionId):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.delete_selection(projectId, selectionId)
        return "Selection deleted", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
