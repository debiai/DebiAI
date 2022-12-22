#############################################################################
# Imports
#############################################################################

import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.DataProviderException as DataProviderException

#############################################################################
# MODELS Management
#############################################################################


def get_results(projectId, modelId, data):
    """
    Get the model results from a sample list
    """
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    try:
        data_provider = data_provider_manager.get_single_data_provider(
            dataProviderId)
        return data_provider.get_model_results(projectId, modelId,  data["sampleIds"]), 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_model(projectId, data):
    """
    Create a new model
    """
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    try:
        data_provider = data_provider_manager.get_single_data_provider(
            dataProviderId)
        data_provider.create_model(projectId, data)
        return "model created", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_model(projectId, data):
    # Create a new model
    projectId = projectId.split("|")[1]
    dataProviderId = "Python module Data Provider"

    try:
        data_provider = data_provider_manager.get_single_data_provider(
            dataProviderId)
        data_provider.create_model(projectId, data)
        return "model created", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def delete_model(projectId, modelId):
    """
    Delete a model
    """
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    try:
        data_provider = data_provider_manager.get_single_data_provider(
            dataProviderId)
        return data_provider.delete_model(projectId, modelId), 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
