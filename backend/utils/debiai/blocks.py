import utils.debiaiUtils as debiaiUtils

dataPath = debiaiUtils.dataPath


def get_tree_from_sampleid_list(projectId, sampleIds):

    # Get path from the hashmap
    samplePath = debiaiUtils.getPathFromHashArray(projectId, sampleIds)

    # Get tree from samples
    return debiaiUtils.getBlockTreeFromSamples(projectId, samplePath)
