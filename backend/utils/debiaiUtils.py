import os
import ujson as json

import utils.utils as utils
import utils.hashUtils as hashUtils

dataPath = "data/"

dataTypes = ["groundTruth",
             "contexts",
             "inputs",
             "others"
             ]


# Init, called at the server start
def init():
    # Create the projects data directory
    try:
        os.mkdir("data")
    except Exception:
        print('Data already initiated')

    # Create the logs folder
    try:
        os.mkdir("logs")
        utils.writeJsonFile("logs/logs.json", [])
    except Exception:
        print('Logs already initiated')

    # TODO: Create a demonstration project

    #  Create the sample hash to path map of each projects
    for projectId in os.listdir(dataPath):
        samplesHashmapPath = dataPath + projectId + "/samplesHashmap.json"
        if utils.fileExist(samplesHashmapPath):
            continue

        print("Creating " + projectId + " samples hashmap")

        projectBLockStructure = getProjectblockLevelInfo(projectId)

        hashmap = {}
        for block in os.listdir(dataPath + projectId + "/blocks"):
            __createProjetHashMap(projectId, block, hashmap, len(
                projectBLockStructure) - 1, 0)

        # Saving the hashmap
        utils.writeJsonFile(samplesHashmapPath, hashmap)


# Projects
def createProject(projectId, projectName):
    # Create the project files and folders
    os.mkdir(dataPath + projectId)
    os.mkdir(dataPath + projectId + "/blocks")
    os.mkdir(dataPath + projectId + "/models")
    os.mkdir(dataPath + projectId + "/requests")
    os.mkdir(dataPath + projectId + "/selections")

    now = utils.timeNow()
    projectInfo = {
        "name": projectName,
        "id": projectId,
        "creationDate": now,
        "updateDate": now,
        "blockLevelInfo": []
    }

    utils.writeJsonFile(dataPath + projectId + '/info.json', projectInfo)
    utils.writeJsonFile(dataPath + projectId + '/samplesHashmap.json', {})


def updateProject(projectId):
    # Change the update date of the project to now
    utils.updateJsonFile(dataPath + projectId + "/info.json",
                         "updateDate", utils.timeNow())


def projectExist(projectId):
    return projectId in os.listdir(dataPath)


def getProjectOverview(projectId):
    try:
        # Json info file
        if not os.path.exists(dataPath + projectId + '/info.json'):
            raise Exception('The "info.json" file is missing')

        with open(dataPath + projectId + '/info.json') as json_file:
            data = json.load(json_file)

        if "name" not in data:
            raise Exception(
                'The project name is missing from the info.json file')

        if "creationDate" not in data:
            raise Exception(
                'The project creationDate is missing from the info.json file')

        if "updateDate" not in data:
            raise Exception(
                'The project updateDate is missing from the info.json file')

        name = data["name"]
        creationDate = data["creationDate"]
        updateDate = data["updateDate"]

        # Nb models
        if not os.path.exists(dataPath + projectId + '/models/'):
            raise Exception('The "models" folder is missing')

        nbModels = len(os.listdir(dataPath + projectId + '/models/'))

        # Nb requests
        nbRequests = 0
        if os.path.exists(dataPath + projectId + '/requests/'):
            nbRequests = len(os.listdir(dataPath + projectId + '/requests/'))

        # Nb selection
        if not os.path.exists(dataPath + projectId + '/selections/'):
            raise Exception('The "selections" folder is missing')

        nbSelection = len(os.listdir(dataPath + projectId + '/selections/'))

        # Nb samples
        if not os.path.exists(dataPath + projectId + '/samplesHashmap.json'):
            raise Exception('The "samplesHashmap.json" file is missing')

        nbSamples = len(getHashmap(projectId))

        # Nb tags
        nbTags = 0
        if os.path.exists(dataPath + projectId + '/tags/'):
            nbTags = len(os.listdir(dataPath + projectId + '/tags/'))

        projectOverview = {
            "id": projectId,
            "name": name,
            "nbModels": nbModels,
            "nbSelections": nbSelection,
            "nbRequests": nbRequests,
            "nbSamples": nbSamples,
            "nbTags": nbTags,
            "creationDate": creationDate,
            "updateDate": updateDate
        }

    except Exception as e:
        projectOverview = {
            "id": projectId,
            "name": projectId,
            "error": True,
            "exeption": str(e)
        }

    return projectOverview


def getProjectsIds():
    projectIds = []

    for projectId in os.listdir(dataPath):
        projectIds.append(projectId)

    return projectIds


def getProjectNameFromId(projectId):
    with open(dataPath + projectId + '/info.json') as json_file:
        return json.load(json_file)['name']


def getProjectblockLevelInfo(projectId):
    if not os.path.isfile(dataPath + projectId + '/info.json'):
        raise Exception("The project '" + projectId +
                        "' doesn't have an info.json file")

    with open(dataPath + projectId + '/info.json') as json_file:
        return json.load(json_file)['blockLevelInfo']


def getResultStructure(projectId):
    with open(dataPath + projectId + '/info.json') as json_file:
        projectInfo = json.load(json_file)
        if "resultStructure" in projectInfo:
            return projectInfo['resultStructure']
        else:
            return None


# Blocks
def blockExist(projectId, blockPath):
    return os.path.isdir(dataPath + projectId + "/blocks/" + blockPath)


def findBlockInfo(projectId, blockPath):

    curPath = dataPath + projectId + "/blocks/" + blockPath

    if not os.path.isdir(curPath):
        return None

    with open(curPath + '/info.json', 'r') as json_file:
        data = json.load(json_file)

    return data


# Tree
def getFirstLevelBlock(projectId, blockId):

    blockList = os.listdir(dataPath + projectId + '/blocks')

    if (blockId not in blockList):
        return -1

    with open(dataPath + projectId + '/blocks/' + blockId + '/info.json')\
            as json_file:
        data = json.load(json_file)

    return data


def getBlockTree(projectId, path, depth):

    childrenBlockNames = utils.listDir(path)
    childrenInfo = []

    if depth > 0:
        # Get the children blocks info
        for name in childrenBlockNames:
            childrenInfo.append(getBlockTree(
                projectId, path + name + "/", depth - 1))

    with open(path + 'info.json') as json_file:
        data = json.load(json_file)
        data['childrenInfoList'] = childrenInfo

    return data


def getBlockTreeFromSamples(projectId, samples: list):
    blocksData = []
    addedBlocks = []

    for samplePath in samples:
        try:
            sampleBlocksData, endLevel = __getBlockTreeFromSample(
                projectId, samplePath, addedBlocks)

            if (endLevel == 0):
                # root block, should be here after added the first sample
                blocksData.append(sampleBlocksData)
            else:
                # Not a root block, we need to find where to insert it
                # First, find the root
                cur = next(
                    block for block in blocksData if block["path"] in sampleBlocksData["path"])

                # Then, find the level
                for i in range(0, endLevel - 1):
                    cur = next(
                        child for child in cur["childrenInfoList"] if child["path"] in sampleBlocksData["path"])

                cur["childrenInfoList"].append(sampleBlocksData)
        except StopIteration as e:
            # TODO : Find why this happens of certain projects
            print("Warning, the sample " + samplePath +
                  " doesn't have a root block")

    return blocksData


def __getBlockTreeFromSample(projectId, blockPath, addedBlocks):
    """
        Go from the botom to the top of a tree
        if at the top or, if block already added, return

    """
    # Add the block we are in
    addedBlocks.append(blockPath)

    with open(dataPath + projectId + "/blocks/" + blockPath + '/info.json') as sampleData:
        info = json.load(sampleData)

    if info["level"] == 0:
        # Top of the tree, end of the recursivity
        return info, 0

    if info["parentPath"] in addedBlocks:
        # The block to the top is already added, there is no need to go further
        return info, info["level"]

    # Climbing up the tree of one level
    parentInfo, endLevel = __getBlockTreeFromSample(
        projectId, info["parentPath"], addedBlocks)

    # Let's add our info to the parents
    cur = parentInfo

    for i in range(endLevel, info["level"] - 1):
        cur = cur["childrenInfoList"][0]
    cur["childrenInfoList"] = [info]

    return parentInfo, endLevel


def addResultsToTree(projectId, tree: list, modelIds: list, commonOnly: bool) -> dict:
    """
        Add, in the tree samples, the results from a model id list
    """

    # Load all the model results
    modelResults = {}
    for modelId in modelIds:
        modelResults[modelId] = getModelResults(projectId, modelId)

    # Get the project block structure
    proBs = getProjectblockLevelInfo(projectId)
    sampleLevel = len(proBs) - 1

    # Add in the samples the results
    for rootBlock in tree:
        __addResultsToABlock(
            rootBlock, modelResults, sampleLevel, commonOnly)

    return tree


def __addResultsToABlock(block, modelResults, sampleLevel, commonOnly):

    if block["level"] == sampleLevel:
        # Adding the results to the sample
        block["results"] = {}
        for modelId in modelResults:
            # If no more than 1 model and commonOnly, no need to check if sample exist in tree
            if commonOnly or len(modelResults) == 1 or block["path"] in modelResults[modelId]:
                block["results"][modelId] = modelResults[modelId][block["path"]]
        return

    for child in block["childrenInfoList"]:
        __addResultsToABlock(child, modelResults, sampleLevel, commonOnly)


# Add samples to a tree
def addBlockTree(projectId, block, blockLevelInfo, blockToAdd, level, parentPath):
    __checkBlockCompliant(block, level, blockLevelInfo)

    # check if block exist
    data = findBlockInfo(projectId, parentPath + block["name"])
    if data is None:
        # BLock doesn't exist
        blockToAdd.append(__createBlock(projectId, block, level, parentPath))

    path = parentPath + block["name"] + "/"

    if level < len(blockLevelInfo) - 1:
        for child in block["childrenInfoList"]:
            addBlockTree(projectId, child, blockLevelInfo,
                         blockToAdd, level + 1, path)


def __checkBlockCompliant(block, level, blockLevelInfo):
    # Check if a block is correct (name exist, levelInfo coherence, etc)

    if "name" not in block:
        raise KeyError("A block at level "
                       + str(level) + " is missing his name")

    # TODO check name valid (no / & .)

    if "childrenInfoList" not in block and level < (len(blockLevelInfo) - 1):
        raise KeyError(
            "Block : " + block["name"] + " has no childrenInfoList properties")

    if level < len(blockLevelInfo) - 1 and len(block["childrenInfoList"]) == 0:
        raise KeyError(
            "Block : " + block["name"] + " has no child block, the tree need to be complet")

    levelInfo = blockLevelInfo[level]

    for type_ in dataTypes:
        if type_ in levelInfo and len(levelInfo[type_]) > 0:
            if type_ not in block:
                raise KeyError(
                    "At least one value of type " + type_ + " is requiered in the block : " + levelInfo["name"])

            if (len(block[type_]) != len(levelInfo[type_])):
                raise KeyError(
                    "Exactly " + str(len(levelInfo[type_])) + " " + type_ + " requiered in the block : " + levelInfo["name"])

            # TODO Implement column default

            for (i, col) in enumerate(levelInfo[type_]):
                if col["type"] == "integer" and type(block[type_][i]) is str:
                    raise KeyError(
                        "Col " + col["name"] + " requier an integer in the block : " + levelInfo["name"])


def __createBlock(projectId, block, level, parentPath):

    blockPath = parentPath + block["name"] + "/"

    debiaiBlock = {
        "id": block["name"],
        "name": block["name"],
        "path": blockPath,
        "parentPath": parentPath,
        "level": level,
        # "creationDate": str(date.today()),
        # "updateDate": str(date.today()),
        # "version": "0.0.0",
        # "metaDataList": {},
    }

    for type_ in dataTypes:
        if type_ in block:
            debiaiBlock[type_] = block[type_]

    return debiaiBlock


def addBlock(projectId, block):
    # create the block folder and his info.json file
    try:
        os.mkdir(dataPath + projectId + "/blocks/" + block["path"])
        utils.writeJsonFile(dataPath + projectId + "/blocks/" +
                            block["path"] + '/info.json', block)
    except FileExistsError:
        print('Warning : The block ' +
              block["path"] + ' already exist, this is not suposed to append')


# Selections
def createSelection(projectId, selectionId, selectionName, sampleHashList, requestId=None):
    selectionInfoFilePath = dataPath + projectId + \
        '/selections/' + selectionId + "/info.json"

    now = utils.timeNow()

    selectionInfo = {
        "id": selectionId,
        "name": selectionName,
        "filePath": selectionInfoFilePath,
        "creationDate": now,
        "updateDate": now,
        "samples": sampleHashList
    }

    if requestId is not None:
        selectionInfo["requestId"] = requestId

    os.mkdir(dataPath + projectId + "/selections/" + selectionId)
    utils.writeJsonFile(selectionInfoFilePath, selectionInfo)
    updateProject(projectId)
    return selectionInfo


def getSelectionIds(projectId):
    return os.listdir(dataPath + projectId + '/selections/')


def selectionExist(projectId, selectionId):
    return selectionId in getSelectionIds(projectId)


def getSelectionInfo(projectId, selectionId):
    with open(dataPath + projectId + "/selections/" + selectionId + "/info.json") as json_file:
        data = json.load(json_file)
        ret = {
            "id": data["id"],
            "name": data["name"],
            "filePath": data["filePath"],
            "creationDate": data["creationDate"],
            "updateDate": data["updateDate"],
            "nbSamples": len(data['samples'])
        }

        # Add the request Id if it exist
        if "requestId" in data:
            ret["requestId"] = data["requestId"]

        return ret


def getSelection(projectId, selectionId):
    # Same as getSelectionInfo but with the samples
    # TODO : set the samples as a csv file
    if not selectionExist(projectId, selectionId):
        return None

    with open(dataPath + projectId + "/selections/" + selectionId + "/info.json") as json_file:
        data = json.load(json_file)
        ret = {
            "id": data["id"],
            "name": data["name"],
            "filePath": data["filePath"],
            "creationDate": data["creationDate"],
            "updateDate": data["updateDate"],
            "nbSamples": len(data['samples']),
            "samples": data['samples']
        }

        # Add the request Id if it exist
        if "requestId" in data:
            ret["requestId"] = data["requestId"]
        return ret


def getSelectionSamples(projectId, selectionId):
    selectionData = getSelection(projectId, selectionId)
    if not selectionData:
        raise KeyError("Selection " + selectionId + " doesn't exist")

    if 'samples' not in selectionData:
        return []
    return selectionData['samples']


def getSelectionsSamples(projectId, selectionIds: list, intersection: bool) -> set:
    if len(selectionIds) == 0:
        return []

    samples = set(getSelectionSamples(projectId, selectionIds[0]))
    for selectionId in selectionIds[1:]:
        if intersection:  # intersection of the selections samples
            samples.intersection_update(
                getSelectionSamples(projectId, selectionId))

            if len(samples) == 0:
                return []
        else:  # Union of the model results samples
            samples = samples.union(
                getSelectionSamples(projectId, selectionId))

    return samples


def deleteSelection(projectId, selectionId):
    utils.deleteDir(dataPath + projectId + "/selections/" + selectionId)
    updateProject(projectId)


#  Models
def getModelIds(projectId):
    return os.listdir(dataPath + projectId + '/models/')


def getModelInfo(projectId, modelId):
    with open(dataPath + projectId + "/models/" + modelId + "/info.json") as json_file:
        return json.load(json_file)


def modelExist(projectId, modelId):
    return modelId in getModelIds(projectId)


def getModelsId(projectId):
    return os.listdir(dataPath + projectId + "/models/")


def deleteModel(projectId, modelId):
    utils.deleteDir(dataPath + projectId + "/models/" + modelId)


def writeModelResults(projectId, modelId, results):
    utils.writeJsonFile(dataPath + projectId + "/models/" +
                        modelId + "/results.json", results)
    updateProject(projectId)


def getModelResults(projectId, modelId, selectionId=None):
    # Get the models results from the project or a selection
    with open(dataPath + projectId + "/models/" + modelId + "/results.json", "r") as jsonFile:
        d = json.load(jsonFile)

    if not selectionId:
        return d
    else:
        selectionSamples = set(getSelectionSamples(projectId, selectionId))
        return selectionSamples.intersection_update(d)


def getModelListResults(projectId, modelIds: list, common: bool) -> list:
    samples = set(getModelResults(projectId, modelIds[0]))

    for modelId in modelIds[1:]:
        if common:  # Common samples between models
            samples.intersection_update(getModelResults(projectId, modelId))
        else:  # Union of the model results samples
            samples = samples.union(getModelResults(projectId, modelId))

    return list(samples)


# hash
def __createProjetHashMap(projectId, blockPath, hashmap, sampleLevel, curentLevel):
    blockPath += "/"
    if curentLevel == sampleLevel:
        # We are at the sample level, we can fill the hashmap
        sampleHash = hashUtils.hash(blockPath)
        hashmap[sampleHash] = blockPath

        # Update the sample
        utils.updateJsonFile(dataPath + projectId + "/blocks/" +
                             blockPath + "info.json", "id", sampleHash)
        return

    for children in utils.listDir(dataPath + projectId + "/blocks/" + blockPath):
        __createProjetHashMap(projectId, blockPath +
                              children, hashmap, sampleLevel, curentLevel + 1)


def addToSampleHashmap(projectId, hashMap):
    with open(dataPath + projectId + '/samplesHashmap.json') as json_file:
        existingHm = json.load(json_file)

    existingHm.update(hashMap)

    utils.writeJsonFile(dataPath + projectId +
                        '/samplesHashmap.json', existingHm)


def getHashmap(projectId):
    with open(dataPath + projectId + '/samplesHashmap.json') as json_file:
        existingHm = json.load(json_file)

    return existingHm


def getPathFromHashArray(projectId, hashArray):
    hm = getHashmap(projectId)
    ret = []
    for hash in hashArray:
        ret.append(hm[hash])
    return ret
