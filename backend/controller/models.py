#############################################################################
# Imports
#############################################################################

import modules.dataProviders.dataProviderManager as data_provider_manager
from modules.dataProviders.DataProviderException import DataProviderException

#############################################################################
# MODELS Management
#############################################################################


def get_results(dataProviderId, projectId, modelId, data):
    """
    Get the model results from a sample list
    """
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return (
            data_provider.get_model_results(projectId, modelId, data["sampleIds"]),
            200,
        )
    except DataProviderException as e:
        return e.message, e.status_code


def post_model(dataProviderId, projectId, data):
    # Create a new model
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.create_model(projectId, data)
        return "model created", 200
    except DataProviderException as e:
        return e.message, e.status_code


def delete_model(dataProviderId, projectId, modelId):
    """
    Delete a model
    """
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.delete_model(projectId, modelId), 200
    except DataProviderException as e:
        return e.message, e.status_code
