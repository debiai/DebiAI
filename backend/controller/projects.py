#############################################################################
# Imports
#############################################################################
import shutil
import ujson as json

import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
import utils.dataProviders as dataProviders
import utils.debiai.projects as projects

dataPath = debiaiUtils.dataPath

#############################################################################
# PROJECTS Management
#############################################################################


def ping():
    return "Online v0.15.1", 200


def log(projectId, data):
    if not debiaiUtils.projectExist(projectId):
        return "Project " + projectId + " not found", 404

    path = 'logs/perfs.json'

    # Get string from json

    f = open(path, "a+")
    f.write(json.dumps(data))
    f.write("\n")
    f.close()

    return 200


# Projects
def upload(upfile):
    # Create a project from a zip file
    import zipfile

    # TODO Check project compliency

    with zipfile.ZipFile(upfile, 'r') as zip_ref:
        zip_ref.extractall(dataPath)

    return 200


def get_projects():
    # return a list of project overviews
    projectOverviews = []

    for projectId in debiaiUtils.getProjectsIds():
        projectOverviews.append(debiaiUtils.getProjectOverview(projectId))

    # Add the data providers views
    projectOverviews += dataProviders.get_projects()

    return projectOverviews, 200


def get_project(projectId):
    # return the info about datasets, models, selections & tags
    if debiaiUtils.projectExist(projectId):
        return projects.getProjectById(projectId), 200

    # Check if the project exists in the data providers
    if dataProviders.projectExist(projectId):
        return dataProviders.getProjectById(projectId), 200

    return "Project " + projectId + " not found", 404


@ utils.traceLog
def post_project(data):
    projectName = data['projectName']

    # Check project name
    if len(projectName) > 50:
        return "Project name too long", 401

    if not utils.is_filename_clean(projectName):
        return "Project name contain invalid characters", 402

    # Create the project ID
    projectId = projectName

    # check duplicate project
    if debiaiUtils.projectExist(projectId):
        return "A project with the name " + projectName + " already exist", 403

    debiaiUtils.createProject(projectId, projectName)

    return debiaiUtils.getProjectOverview(projectId), 200


@ utils.traceLog
def delete_project(projectId):
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    try:
        shutil.rmtree(dataPath + projectId)
    except Exception as e:
        print(e)
        return "Something went wrong when deleting the project", 500

    return "ok", 200


# Blocklevel
@ utils.traceLog
def post_blocklevels(projectId, blocklevels):

    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # TODO : check blocklevels

    # save blocklevels
    utils.updateJsonFile(dataPath + projectId + '/info.json',
                         "blockLevelInfo", blocklevels)

    return blocklevels, 200


# Expected_results
@ utils.traceLog
def post_resultsStructure(projectId, resultStructure):
    # Add the expecter results structure
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # TODO : check resultStructure (type and default type ==)

    existingResultStructure = debiaiUtils.getResultStructure(projectId)
    if existingResultStructure is not None:
        return "project " + projectId + " already have a results structure", 403

    # save resultStructure
    utils.updateJsonFile(dataPath + projectId + '/info.json',
                         "resultStructure", resultStructure)
    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


@ utils.traceLog
def post_addExpectedResult(projectId, resultColumn):
    # Add acolumn to the expecter results structure
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    resultStructure = debiaiUtils.getResultStructure(projectId)

    if resultStructure is None:
        return "project " + projectId + " does not have a results structure", 403

    # TODO : check resultStructure (type and default type ==)

    resultStructure.append(resultColumn)

    # save updated resultStructure
    utils.updateJsonFile(dataPath + projectId + '/info.json',
                         "resultStructure", resultStructure)

    # add to each results the default value
    for modelId in debiaiUtils.getModelsId(projectId):
        results = debiaiUtils.getModelResults(projectId, modelId)

        for key in results:
            results[key].append(resultColumn["default"])

        debiaiUtils.writeModelResults(projectId, modelId, results)

    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


@ utils.traceLog
def delete_expectedResult(projectId, resultColumn):
    # Add acolumn to the expecter results structure
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    resultStructure = debiaiUtils.getResultStructure(projectId)

    if resultStructure is None:
        return "project " + projectId + " does not have a results structure", 403

    # TODO : check resultStructure (type and default type ==)

    length_results = len(resultStructure)
    idx = -1
    resultColumn = resultColumn["value"]

    for i in range(length_results):
        if resultStructure[i]["name"] == resultColumn:
            resultStructure.pop(i)
            idx = i
            break

    if idx == -1:
        return "Columns " + resultColumn + " does not exists.", 404

    # save updated resultStructure
    utils.updateJsonFile(dataPath + projectId + '/info.json',
                         "resultStructure", resultStructure)

    # add to each results the default value
    for modelId in debiaiUtils.getModelsId(projectId):
        results = debiaiUtils.getModelResults(projectId, modelId)

        for key in results:
            results[key].pop(idx)

        debiaiUtils.writeModelResults(projectId, modelId, results)

    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


@ utils.traceLogLight
def check_hash(projectId, data):
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    hash_list = data['hash_list']

    hashmap = debiaiUtils.getHashmap(projectId)

    not_valide = []

    for hash in hash_list:
        if hash not in hashmap:
            not_valide.append(hash)

    return not_valide, 200
