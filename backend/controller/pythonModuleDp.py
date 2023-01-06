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
    # TODO : fix
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    data_provider.add_results_dict(projectId, modelId, data)
    return "Model deleted", 200


def add_results_hash(project_id, modelId, data):
    if not projects.project_exist(project_id):
        return "Project '" + project_id + "' doesn't exist", 404

    if not model_exist(project_id, modelId):
        return (
            "Dataset '"
            + modelId
            + "' in project : '"
            + projects.getProjectNameFromId(project_id)
            + "' doesnk't exist",
            404,
        )

    # Get hash-result dic
    results = data["results"]

    # Get hash-path dic
    hashmap = hash.getHashmap(project_id)

    # Get all keys
    keys = []
    for key in results:
        keys.append(key)

    # Change hash by path in dic
    for key in keys:
        path = hashmap[key]
        results[path] = results.pop(key)

    newResults = utils.addToJsonFIle(
        dataPath + project_id + "/models/" + modelId + "/results.json", results
    )
    utils.addToJsonFIle(
        dataPath + project_id + "/models/" + modelId + "/info.json",
        {"nbResults": len(newResults), "updateDate": utils.timeNow()},
    )

    debiaiUtils.update_project(project_id)
    return 200
