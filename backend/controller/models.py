#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager

#############################################################################
# MODELS Management
#############################################################################


def get_models(projectId):
    ret = []
    return ret, 200


def get_results(projectId, modelId, data):
    """
    Get the model results from a sample list
    """
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)
    return data_provider.get_model_results(projectId, modelId,  data["sampleIds"]), 200
