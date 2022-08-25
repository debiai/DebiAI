import utils.debiaiUtils as debiaiUtils

dataPath = debiaiUtils.dataPath


def getProjectById(projectId):
    projectInfo = debiaiUtils.getProjectOverview(projectId)

    # Add the selections
    projectInfo["selections"] = []
    for selectionId in debiaiUtils.getSelectionIds(projectId):
        projectInfo["selections"].append(
            debiaiUtils.getSelectionInfo(projectId, selectionId))

    # Add the models
    projectInfo["models"] = []
    for modelId in debiaiUtils.getModelIds(projectId):
        projectInfo["models"].append(
            debiaiUtils.getModelInfo(projectId, modelId))

    # Add the block structure
    projectInfo["blockLevelInfo"] = debiaiUtils.getProjectblockLevelInfo(
        projectId)

    # Add the results structure
    projectInfo["resultStructure"] = debiaiUtils.getResultStructure(
        projectId)

    return projectInfo
