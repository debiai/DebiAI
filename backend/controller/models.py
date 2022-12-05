#############################################################################
# Imports
#############################################################################
import os
import ujson as json

#import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
import utils.dataProviders as dataProviders

#dataPath = debiaiUtils.dataPath

#############################################################################
# MODELS Management
#############################################################################


#@utils.traceLogLight
def get_models(projectId):
    ret = []

    # TODO data_providers


#@utils.traceLog
def post_model(projectId, data):

    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    modelId = data["name"]

    if not utils.is_filename_clean(modelId):
        return "Model name contain prohibed caracters", 402

    if debiaiUtils.modelExist(projectId, modelId):
        return "Model '" + modelId + "' already exist", 201

    metadata = {}
    if "metadata" in data:
        metadata = data["metadata"]

    # model
    modelFolderPath = dataPath + projectId + "/models/" + modelId
    os.mkdir(modelFolderPath)

    now = utils.timeNow()

    modelInfo = {
        "name": modelId,
        "id": modelId,
        "creationDate": now,
        "updateDate": now,
        "metadata": metadata,
        "nbResults": 0,
    }

    utils.writeJsonFile(modelFolderPath + "/info.json", modelInfo)
    debiaiUtils.writeModelResults(projectId, modelId, {})

    return modelInfo, 200


#@utils.traceLog
def delete_model(projectId, modelId):
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    if not debiaiUtils.modelExist(projectId, modelId):
        return "The model doesn't exist", 404

    debiaiUtils.deleteModel(projectId, modelId)

    return "ok", 200


#@utils.traceLogLight
def add_results_dict(projectId, modelId, data):

    tree = data["results"]

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    if not debiaiUtils.modelExist(projectId, modelId):
        return (
            "Dataset '"
            + modelId
            + "' in project : '"
            + debiaiUtils.getProjectNameFromId(projectId)
            + "' doesn't exist",
            404,
        )

    # Get resultStructure & project_block_structure
    result_structure = debiaiUtils.getResultStructure(projectId)
    if result_structure is None:
        return (
            "The project expected results need to be specified before adding results",
            403,
        )

    if "expected_results_order" in data:
        expected_results_order = data["expected_results_order"]
    else:
        expected_results_order = list(map(lambda r: r["name"], result_structure))

    project_block_structure = debiaiUtils.getProjectblockLevelInfo(projectId)
    sampleIndex = len(project_block_structure) - 1

    # Check the given expected_results_order
    for expected_result in result_structure:
        if expected_result["name"] not in expected_results_order:
            return (
                "The expected result '"
                + expected_result["name"]
                + "' is missing from the expected_results_order Array",
                403,
            )

    giv_exp_res = {}
    for given_expected_result in expected_results_order:
        result_expected = False
        for (i, expected_result) in enumerate(result_structure):
            if given_expected_result == expected_result["name"]:
                result_expected = True

                # Map the expected_results_order indexes to result_structure
                giv_exp_res[given_expected_result] = i

        if not result_expected:
            return (
                "The given expected result '"
                + given_expected_result
                + "' is not an expected result",
                403,
            )

    #  Check if all blocks referenced in the result tree exists
    resultsToAdd = {}

    for blockKey in tree:
        ok, msg = __check_blocks_of_tree_exists(
            projectId,
            result_structure,
            giv_exp_res,
            tree[blockKey],
            0,
            sampleIndex,
            blockKey,
            resultsToAdd,
        )
        if not ok:
            print(msg)
            return msg, 403

    # The given tree is complient, let's add the results
    newResults = utils.addToJsonFIle(
        dataPath + projectId + "/models/" + modelId + "/results.json", resultsToAdd
    )

    utils.addToJsonFIle(
        dataPath + projectId + "/models/" + modelId + "/info.json",
        {"nbResults": len(newResults), "updateDate": utils.timeNow()},
    )
    debiaiUtils.updateProject(projectId)
    return 200


def __check_blocks_of_tree_exists(
    projectId: str,
    result_structure: list,
    giv_exp_res: dict,
    block: dict,
    level: int,
    sampleIndex: int,
    path: str,
    resultsToAdd: dict,
):

    # Check block exist in the data
    blockInfo = debiaiUtils.findBlockInfo(projectId, path)
    if not blockInfo:
        return (
            False,
            "Error while adding the results : block '" + path + "' doesn't exist",
        )

    if level == sampleIndex:
        path += "/"
        resultsToAdd[blockInfo["id"]] = []
        #  Sample level : the results : they need to be verified
        if len(block) != len(giv_exp_res):
            raise ValueError(
                "in : "
                + path
                + ", "
                + str(len(block))
                + " value where given but "
                + str(len(giv_exp_res))
                + "where expected"
            )

        for result in result_structure:
            resultsToAdd[blockInfo["id"]].append(block[giv_exp_res[result["name"]]])
            # TODO Deal with defaults results and check type

        return True, None

    for subBlockKey in block:
        ok, msg = __check_blocks_of_tree_exists(
            projectId,
            result_structure,
            giv_exp_res,
            block[subBlockKey],
            level + 1,
            sampleIndex,
            path + "/" + str(subBlockKey),
            resultsToAdd,
        )
        if not ok:
            return False, msg

    return True, ""


#@utils.traceLog
def add_results_hash(projectId, modelId, data):
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    if not debiaiUtils.modelExist(projectId, modelId):
        return (
            "Dataset '"
            + modelId
            + "' in project : '"
            + debiaiUtils.getProjectNameFromId(projectId)
            + "' doesn't exist",
            404,
        )

    # Get hash-result dic
    results = data["results"]

    # Get hash-path dic
    hashmap = debiaiUtils.getHashmap(projectId)

    # Get all keys
    keys = []
    for key in results:
        keys.append(key)

    # Change hash by path in dic
    for key in keys:
        path = hashmap[key]
        results[path] = results.pop(key)

    newResults = utils.addToJsonFIle(
        dataPath + projectId + "/models/" + modelId + "/results.json", results
    )
    utils.addToJsonFIle(
        dataPath + projectId + "/models/" + modelId + "/info.json",
        {"nbResults": len(newResults), "updateDate": utils.timeNow()},
    )

    debiaiUtils.updateProject(projectId)
    return 200


#@utils.traceLogLight
def get_results(projectId, modelId, data):
    """
    Get the model results from a sample list
    """
    sampleIds = data["sampleIds"]

    # Check parameters
    if debiaiUtils.projectExist(projectId):
        if debiaiUtils.modelExist(projectId, modelId):
            # Get model results
            modelResults = debiaiUtils.getModelResults(projectId, modelId)
            ret = {}
            for sampleId in sampleIds:
                if sampleId in modelResults:
                    ret[sampleId] = modelResults[sampleId]
            return ret, 200
        else:
            return "Model " + modelId + " does not exist", 404

    if dataProviders.projectExist(projectId):
        if dataProviders.modelExist(projectId, modelId):
            # Get model results
            modelResults = dataProviders.getModelResults(projectId, modelId, sampleIds)
            return modelResults, 200
        else:
            return "Model " + modelId + " does not exist", 404

    return "Project '" + projectId + "' doesn't exist", 404
