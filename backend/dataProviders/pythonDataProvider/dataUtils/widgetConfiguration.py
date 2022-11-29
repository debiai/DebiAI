import os
import ujson as json
import utils.debiaiUtils as debiaiUtils
import utils.utils as utils

dataPath = debiaiUtils.dataPath


def getConfigurations(projectId):
    try:
        with open(dataPath + projectId + "/analysis/widgetConfigurations.json") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        try:
            saveConfigurations(projectId, {})
        except FileNotFoundError:
            os.mkdir(dataPath + projectId + "/analysis")
            saveConfigurations(projectId, {})


def createConfiguration(projectId, widgetTitle, confName, conf):
    confFile = getConfigurations(projectId)
    if widgetTitle not in confFile:
        confFile[widgetTitle] = {}

    confFile[widgetTitle][confName] = conf

    saveConfigurations(projectId, confFile)


def saveConfigurations(projectId, conf):
    utils.writeJsonFile(dataPath + projectId +
                        "/analysis/widgetConfigurations.json", conf)
    debiaiUtils.updateProject(projectId)


def deleteConfiguration(projectId, widgetTitle, confName):
    confFile = getConfigurations(projectId)
    if widgetTitle in confFile:
        if confName in confFile[widgetTitle]:
            del confFile[widgetTitle][confName]
            saveConfigurations(projectId, confFile)
