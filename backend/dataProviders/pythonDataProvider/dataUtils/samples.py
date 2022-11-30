import utils
import hash
import tree
import selections
import models
import projects
DATA_PATH = utils.DATA_PATH

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
        modelSamples = models.getModelListResults(
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


# Get data
def get_tree_from_sampleid_list(projectId, sampleIds):
    # Get path from the hashmap
    samplePath = hash.getPathFromHashList(projectId, sampleIds)

    # Get tree from samples
    return tree.getBlockTreeFromSamples(projectId, samplePath)


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


# def getBlockInfo(blockLevel, blockInfo):
#     """
#     Convert the block info to fill the sampleInfo list with a colonName:value dict
#     """
#     ret = {}
#     ret[blockLevel["name"]] = blockInfo["name"]

#     for dataType in utils.DATA_TYPES:
#         if dataType in blockLevel:
#             for (i, column) in enumerate(blockLevel[dataType]):
#                 ret[column['name']] = blockInfo[dataType][i]

#     return ret
