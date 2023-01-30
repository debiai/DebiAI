import dataProviders.DataProviderException as DataProviderException
import dataProviders.dataProviderManager as data_provider_manager


# Blocklevel
def post_blocklevels(projectId, blocklevels):
    projectId = projectId.split("|")[1]
    dataProviderId = "Python module Data Provider"
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    try:
        data_provider.update_block_structure(projectId, blocklevels)
        return blocklevels, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


# Expected_results
def post_resultsStructure(projectId, resultStructure):
    # Add the expected results structure
    projectId = projectId.split("|")[1]
    dataProviderId = "Python module Data Provider"
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    try:
        data_provider.update_results_structure(projectId, resultStructure)
        return resultStructure, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_block_tree(projectId, data):
    # Add data to a project from a tree
    projectId = projectId.split("|")[1]
    dataProviderId = "Python module Data Provider"
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    try:
        return data_provider.add_block_tree(projectId, data), 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


# Add model results
def add_results_dict(projectId, modelId, data):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    data_provider.add_results_dict(projectId, modelId, data)
    return "Model deleted", 200
