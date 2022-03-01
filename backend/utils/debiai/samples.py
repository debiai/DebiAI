import utils.debiaiUtils as debiaiUtils
import utils.utils as utils

dataPath = debiaiUtils.dataPath


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
