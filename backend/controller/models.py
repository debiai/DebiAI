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


# Python module specific function:
def post_model(projectId, data):
    # Create a new model
    # TODO check that this data provider has been enabled
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)
    data_provider.add_model(projectId, data)
    return "Model added", 200


def delete_model(projectId, modelId):
    #TODO : fix
    # Delete a model
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)
    data_provider.delete_model(projectId, modelId)
    return "Model deleted", 200


def add_results_dict(projectId, modelId, data):
    #TODO : fix
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)
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

    debiaiUtils.updateProject(project_id)
    return 200
