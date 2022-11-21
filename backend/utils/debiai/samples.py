import utils.debiaiUtils as debiaiUtils
import utils.utils as utils

dataPath = debiaiUtils.dataPath


def get_list(projectId, data):
    """
    Return a list of samples in a project
    """

    # Get the hashmap
    hashmap = debiaiUtils.getHashmap(projectId)

    # Get params
    selectionIds = data["selectionIds"]
    selectionIntersection = data["selectionIntersection"]
    modelIds = data["modelIds"]
    commonResults = data["commonResults"]

    if not selectionIds or len(selectionIds) == 0:
        # Start form all the project samples
        sample = hashmap.keys()
        # In case of streaming purpose
        if "from" in data and "to" in data:
            sample = sample[data["from"]: data["to"]]
    else:
        # Or from the selections samples
        try:
            samples = debiaiUtils.getSelectionsSamples(
                projectId, selectionIds, selectionIntersection)
        except KeyError as e:
            print(e)
            return "selection not found", 404

    if len(samples) == 0:
        return {
            "samples": [],
            "nbSamples": 0,
            "nbFromSelection": 0,
            "nbFromModels": 0
        }

    nbFromSelection = len(samples)
    nbFromModels = 0
    # Then, concat with the model results if given
    if modelIds and len(modelIds) > 0:
        modelSamples = debiaiUtils.getModelListResults(
            projectId, modelIds, commonResults)
        nbFromModels = len(modelSamples)
        samples = set(samples)
        samples.intersection_update(set(modelSamples))

    return {
        "samples": list(samples),
        "nbSamples": len(samples),
        "nbFromSelection": nbFromSelection,
        "nbFromModels": nbFromModels
    }


def projectSamplesGerenator(projectId):
    """
    Generator used to iterate over all samples in a project.
    Used by the 'createSelectionFromRequest' method
    """

    # Get the project block structure
    projectBlockStructure = debiaiUtils.getProjectblockLevelInfo(projectId)
    sampleLevel = len(projectBlockStructure) - 1

    rootBlocks = utils.listDir(dataPath + projectId + "/blocks/")
    for rootBlock in rootBlocks:
        path = dataPath + projectId + "/blocks/" + rootBlock + "/"
        yield from yieldSample(path,  0, [], sampleLevel, projectBlockStructure)
    print("end")


def yieldSample(path, level, sampleInfo, sampleLevel, blockLevelInfo):
    # TODO : optimisations : add in parameters the block that we need to open
    blockInfo = utils.readJsonFile(path + "info.json")
    sampleInfo.append(getBlockInfo(blockLevelInfo[level], blockInfo))

    if level == sampleLevel:
        # merge the dict into one
        yield {k: v for x in sampleInfo for k, v in x.items()}, blockInfo["id"]
    else:
        childrenBlockNames = utils.listDir(path)
        for name in childrenBlockNames:
            yield from yieldSample(path + name + "/",
                                   level + 1, sampleInfo, sampleLevel, blockLevelInfo)
            del sampleInfo[-1]


def getBlockInfo(blockLevel, blockInfo):
    """
    Convert the block info to fill the sampleInfo list with a colonName:value dict
    """
    ret = {}
    ret[blockLevel["name"]] = blockInfo["name"]

    for dataType in debiaiUtils.dataTypes:
        if dataType in blockLevel:
            for (i, column) in enumerate(blockLevel[dataType]):
                ret[column['name']] = blockInfo[dataType][i]

    return ret
