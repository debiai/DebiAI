#############################################################################
# Imports
#############################################################################
import os

#import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
#import utils.hashUtils as hashUtils
import utils.dataProviders as dataProviders
import dataProviders.dataProviderManager as data_provider_manager


#import utils.debiai.blocks as blocksUtils

#dataPath = debiaiUtils.dataPath

#############################################################################
# BLOCK Management
#############################################################################


# Blocks to tree
def get_block_racine(projectId, depth):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Get the first level blocks
    blockList = os.listdir(dataPath + projectId + "/blocks")

    blocksData = []

    for blockId in blockList:
        blockPath = dataPath + projectId + "/blocks/" + blockId + "/"
        blocksData.append(debiaiUtils.getBlockTree(projectId, blockPath, depth))

    return blocksData, 200


def get_block_racine_from_selection(projectId, selectionId, depth):
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Load selection sample list
    selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

    if not selectionDetails:
        return "Selection " + selectionId + " not found", 404

    if len(selectionDetails["samples"]) == 0:
        return []

    # Converting samples hash into path
    hashList = debiaiUtils.getHashmap(projectId)
    for i in range(len(selectionDetails["samples"])):
        selectionDetails["samples"][i] = hashList[selectionDetails["samples"][i]]

    # Get the tree
    tree = debiaiUtils.getBlockTreeFromSamples(projectId, selectionDetails["samples"])

    return tree, 200


def get_block_tree(projectId, data):
    blockId = data["blockId"]
    blockPath = data["blockPath"]
    depth = data["depth"]

    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    path = dataPath + projectId + "/blocks/" + blockPath

    blockInfo = debiaiUtils.findBlockInfo(projectId, blockPath)

    if blockInfo is None:
        return "Block '" + blockId + "' doesn't exist", 404

    blockTree = debiaiUtils.getBlockTree(projectId, path, depth)

    return blockTree, 200


def get_tree_with_model_results(projectId, data):
    # return a tree from root with wanted model results in the samples

    modelIds = data["modelIds"]
    #  if common true : get the model common samples, else, get union
    common = data["common"]

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    for modelId in modelIds:
        if not debiaiUtils.modelExist(projectId, modelId):
            return "Model " + modelId + " does not exist", 403

    # Get model results samples
    samples = debiaiUtils.getModelListResults(projectId, modelIds, common)

    # Get tree from samples
    tree = debiaiUtils.getBlockTreeFromSamples(projectId, samples)

    # Add the model results to the tree samples
    debiaiUtils.addResultsToTree(projectId, tree, modelIds, common)
    return tree, 200


def get_tree_from_sampleid_list(data_provider_id, projectId, data):
    # return a tree from a list of sample ID
    sampleIds = data["sampleIds"]

    data_provider = data_provider_manager.get_single_data_provider(data_provider_id)
    
    samples = data_provider.get_samples(projectId, sampleIds)
    
    if samples is not None:
        return samples, 200
    
    
        
    # # Check parameters
    # if debiaiUtils.projectExist(projectId):
    #     return blocksUtils.get_tree_from_sampleid_list(projectId, sampleIds), 200

    # if dataProviders.projectExist(projectId):
    #     return dataProviders.get_data(projectId, sampleIds), 200

    return "Can't find samples for project " + projectId + " on data provider : " + data_provider_id, 404


# Training samples
def get_training_samples_number(projectId, selectionId=None):
    # return a the number of data to pull

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    projectHashMap = debiaiUtils.getHashmap(projectId)

    # Get samples
    if selectionId:
        # Load selection sample list
        selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

        if not selectionDetails:
            return "Selection " + selectionId + " not found", 404

        hashListToReturn = selectionDetails["samples"]
    else:
        hashListToReturn = list(projectHashMap.keys())

    return len(hashListToReturn), 200


def get_training_samples_number_with_model_results(
    projectId, modelIds, common, selectionId=None
):
    # return a the number of data to pull but with models

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    for modelId in modelIds:
        if not debiaiUtils.modelExist(projectId, modelId):
            return "Model " + modelId + " does not exist", 403

    if selectionId:
        # Load selection sample list
        selectionDetails = debiaiUtils.getSelection(projectId, selectionId)
        if not selectionDetails:
            return "Selection " + selectionId + " not found", 404

    # Get model results samples
    samples = debiaiUtils.getModelListResults(projectId, modelIds, common, selectionId)

    return len(samples), 200


def get_training_samples(projectId, start, size, selectionId=None):
    # return a list of samples
    # from a start position and a size

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    projectHashMap = debiaiUtils.getHashmap(projectId)

    # Get samples
    if selectionId:
        # Load selection sample list
        selectionDetails = debiaiUtils.getSelection(projectId, selectionId)

        if not selectionDetails:
            return "Selection " + selectionId + " not found", 404

        hashListToReturn = selectionDetails["samples"][start : start + size]
    else:
        hashListToReturn = list(projectHashMap.keys())[start : start + size]

    # Convert hash to sample path
    for i in range(len(hashListToReturn)):
        hashListToReturn[i] = projectHashMap[hashListToReturn[i]]

    tree = debiaiUtils.getBlockTreeFromSamples(projectId, hashListToReturn)

    return tree, 200


def get_training_samples_with_model_results(
    projectId, start, size, modelIds, common, selectionId=None
):
    # return a tree chunk from root or a selection
    # with wanted model results in the samples

    # Check parameters
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    for modelId in modelIds:
        if not debiaiUtils.modelExist(projectId, modelId):
            return "Model " + modelId + " does not exist", 403

    if selectionId:
        # Load selection sample list
        selectionDetails = debiaiUtils.getSelection(projectId, selectionId)
        if not selectionDetails:
            return "Selection " + selectionId + " not found", 404

    # Get model results samples
    samples = debiaiUtils.getModelListResults(projectId, modelIds, common, selectionId)

    # Crop the samples for the chunk
    samples = list(samples)[start : start + size]

    # Get tree from samples
    tree = debiaiUtils.getBlockTreeFromSamples(projectId, samples)

    # Add the model results to the tree samples
    debiaiUtils.addResultsToTree(projectId, tree, modelIds, common)
    return tree, 200


# Others
def post_block_tree(projectId, data):
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project not found", 404

    # Loading project block info
    bli = debiaiUtils.getProjectblockLevelInfo(projectId)

    # going through the tree to check for error, store the block to add
    blockToAdd = []

    try:
        for block in data["blockTree"]:
            debiaiUtils.addBlockTree(projectId, block, bli, blockToAdd, 0, "")
    except KeyError as e:
        print(str(e))
        print("badInputTree")
        return str(e), 403

    if len(blockToAdd) == 0:
        return "No block added", 201

    # Store the blocks and the hash map
    sampleLevel = len(bli) - 1
    hashToSave = {}
    for block in blockToAdd:

        if block["level"] == sampleLevel:
            # Sample level, creating hash
            sampleHash = hashUtils.hash(block["path"])
            block["id"] = sampleHash
            hashToSave[sampleHash] = block["path"]

        debiaiUtils.addBlock(projectId, block)

    # Save hashmap
    debiaiUtils.addToSampleHashmap(projectId, hashToSave)

    debiaiUtils.updateProject(projectId)
    return str(len(blockToAdd)) + " added blocks", 200


def delete_block(projectId, blockId, blockPath):

    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    blockInfo = debiaiUtils.findBlockInfo(projectId, blockPath)

    if blockInfo is None:
        return "Block '" + blockId + "' doesn't exist", 404

    utils.deleteDir(blockPath)
    debiaiUtils.updateProject(projectId)
    return "ok", 200
