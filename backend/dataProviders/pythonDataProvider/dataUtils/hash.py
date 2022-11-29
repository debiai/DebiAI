import hashlib
import ujson as json

from backend.dataProviders.pythonDataProvider.dataUtils import utils
DATA_PATH = utils.DATA_PATH

def hash(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# hash
def __createProjetHashMap(projectId, blockPath, hashmap, sampleLevel, curentLevel):
    blockPath += "/"
    if curentLevel == sampleLevel:
        # We are at the sample level, we can fill the hashmap
        sampleHash = hash(blockPath)
        hashmap[sampleHash] = blockPath

        # Update the sample
        utils.updateJsonFile(DATA_PATH + projectId + "/blocks/" +
                             blockPath + "info.json", "id", sampleHash)
        return

    for children in utils.listDir(DATA_PATH + projectId + "/blocks/" + blockPath):
        __createProjetHashMap(projectId, blockPath +
                              children, hashmap, sampleLevel, curentLevel + 1)


def addToSampleHashmap(projectId, hashMap):
    with open(DATA_PATH + projectId + '/samplesHashmap.json') as json_file:
        existingHm = json.load(json_file)

    existingHm.update(hashMap)

    utils.writeJsonFile(DATA_PATH + projectId +
                        '/samplesHashmap.json', existingHm)


def getHashmap(projectId):
    with open(DATA_PATH + projectId + '/samplesHashmap.json') as json_file:
        existingHm = json.load(json_file)

    return existingHm


def getPathFromHashArray(projectId, hashArray):
    hm = getHashmap(projectId)
    ret = []
    for hash in hashArray:
        ret.append(hm[hash])
    return ret
