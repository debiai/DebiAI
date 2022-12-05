from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils, selections, models, selections, tree, hash

DATA_PATH = pythonModuleUtils.DATA_PATH
DATA_TYPES = pythonModuleUtils.DATA_TYPES

# ID list


def get_all_samples_id_list(project_id, _from=None, _to=None):
    """
    Return a list of all samples id in a project
    """
    # Get the hashmap
    hashmap = hash.getHashmap(project_id)

    # Get all samples
    samples = list(hashmap.keys())

    # In case of streaming purpose
    if _from is not None and _to is not None:
        samples = samples[_from: _to + 1]

    return samples


def get_list(projectId, data):
    """
    Return a list of samples in a project
    """

    # Get the hashmap
    hashmap = hash.getHashmap(projectId)

    # Get params
    selectionIds = data["selectionIds"]
    selectionIntersection = data["selectionIntersection"]
    modelIds = data["modelIds"]
    commonResults = data["commonResults"]

    samples = []
    if not selectionIds or len(selectionIds) == 0:
        # Start form all the project samples
        samples = list(hashmap.keys())
        # In case of streaming purpose
        if "from" in data and "to" in data:
            samples = samples[data["from"]: data["to"] + 1]
    else:
        # Or from the selections samples
        try:
            samples = selections.getSelectionsSamples(
                projectId, selectionIds, selectionIntersection
            )
        except KeyError as e:
            print(e)
            return "selection not found", 404

    if len(samples) == 0:
        return {"samples": [], "nbSamples": 0, "nbFromSelection": 0, "nbFromModels": 0}

    nbFromSelection = len(samples)
    nbFromModels = 0
    # Then, concat with the model results if given
    if modelIds and len(modelIds) > 0:
        modelSamples = models.getModelListResults(
            projectId, modelIds, commonResults)
        nbFromModels = len(modelSamples)
        samples = set(samples)
        samples.intersection_update(set(modelSamples))

    return {
        "samples": list(samples),
        "nbSamples": len(samples),
        "nbFromSelection": nbFromSelection,
        "nbFromModels": nbFromModels,
    }


# Get data
def get_data_from_sampleid_list(project_id, id_list):
    # Get path of the samples from the hashmap
    sample_path = hash.getPathFromHashList(project_id, id_list)[:10]

    # Get tree from samples
    samples_tree = tree.getBlockTreeFromSamples(project_id, sample_path)

    # Convert tree to array
    data_array = _tree_to_array(samples_tree)

    # Convert array to dict
    data = {}
    for i in range(len(id_list)):
        data[id_list[i]] = data_array[i]

    return data


def _tree_to_array(tree):
    data_array = []
    for block in tree:
        data_array += _block_to_array_recur(block)
    return data_array


def _get_block_values(block):
    # Adding the block name into the values
    values = []

    # store all key-values into an array
    for data_type in DATA_TYPES:
        if (data_type in block):
            for key in range(len(block[data_type])):
                values.append(block[data_type][key])

    return values


def _block_to_array_recur(block):
    # Getting bloc values
    values = _get_block_values(block)
    if "childrenInfoList" not in block or len(block["childrenInfoList"]) == 0:
        return [values]

    else:
        # Getting all child values
        child_values = []
        for child_block in block["childrenInfoList"]:
            child_values.append(_block_to_array_recur(child_block))

        # Mergin childs and current block values
        #     CurBlock childs
        #     a        1
        #     a        2
        #     a        3

        #     b        1
        #     b        2
        #     b        3

        array = []
        for child_val in child_values:
            print("========")
            array.append(values + child_val[0])
            print(values + child_val[0])
        return array


# def projectSamplesGerenator(projectId):
#     """
#     Generator used to iterate over all samples in a project.
#     Used by the 'createSelectionFromRequest' method
#     """

#     # Get the project block structure
#     projectBlockStructure = projects.getProjectblockLevelInfo(projectId)
#     sampleLevel = len(projectBlockStructure) - 1

#     rootBlocks = utils.listDir(DATA_PATH + projectId + "/blocks/")
#     for rootBlock in rootBlocks:
#         path = DATA_PATH + projectId + "/blocks/" + rootBlock + "/"
#         yield from yieldSample(path,  0, [], sampleLevel, projectBlockStructure)
#     print("end")


# def yieldSample(path, level, sampleInfo, sampleLevel, blockLevelInfo):
#     # TODO : optimisations : add in parameters the block that we need to open
#     blockInfo = utils.readJsonFile(path + "info.json")
#     sampleInfo.append(getBlockInfo(blockLevelInfo[level], blockInfo))

#     if level == sampleLevel:
#         # merge the dict into one
#         yield {k: v for x in sampleInfo for k, v in x.items()}, blockInfo["id"]
#     else:
#         childrenBlockNames = utils.listDir(path)
#         for name in childrenBlockNames:
#             yield from yieldSample(path + name + "/",
#                                    level + 1, sampleInfo, sampleLevel, blockLevelInfo)
#             del sampleInfo[-1]
