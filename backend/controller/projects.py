#############################################################################
# Imports
#############################################################################
import shutil
import ujson as json

import utils.utils as utils
import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.pythonDataProvider.dataUtils.pythonModuleUtils as moduleUtils
import dataProviders.pythonDataProvider.dataUtils.projects as projectUtils

#############################################################################
# PROJECTS Management
#############################################################################

def ping():
    return "Online v0.15.1", 200


def get_projects():
    # return a list of project overviews
    # todo : Faire marcher avec internal data provider
    data_providers_list = data_provider_manager.get_data_provider_list()
    projectOverviews = []
    for data_provider in data_providers_list:
        projects = data_provider.get_projects()
        if projects is not None:
            # TMP: merging dp ids and project ids TODO: change this
            for project in projects:
                project["id"] = data_provider.name + "|" + project["id"]
            projectOverviews.extend(projects)

    return projectOverviews, 200


def get_project(projectId):
    # return the info about datasets, models, selections & tags
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    project = data_provider.get_project(projectId)
    if project is not None:
        project["id"] = dataProviderId + "|" + project["id"]
        return project, 200
    
    return "Project " + projectId + " on data Provider " + dataProviderId + " not found", 404
    
    
def post_project(data):
    projectName = data["projectName"]
    
    data_provider = data_provider_manager.get_single_data_provider("Python module Data Provider")

    ### Todo : voir si les checks ici ou dans des Use Cases
    
    # Check project name
    if len(projectName) > 50:
        return "Project name too long", 401

    if not moduleUtils.is_filename_clean(projectName):
        return "Project name contain invalid characters", 402 
    
    # check duplicate project
    if projectUtils.project_exist(projectName):
        return "A project with the name " + projectName + " already exist", 403
      
    # Create the project ID
    projectId = projectName
    
    project = data_provider.create_project(projectId)
    print(project)
    return project, 200
    

def delete_project(projectId):
    print(projectId)
    if not projectUtils.project_exist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404
    
    data_provider = data_provider_manager.get_single_data_provider("Python module Data Provider")
    
    try:
        data_provider.delete_project(projectId)    
    except Exception as e:
        print(e)
        return "Something went wrong when deleting the project", 500

    return "ok", 200


# Blocklevel
def post_blocklevels(projectId, blocklevels):
    #### Todo : Virer quand l'api aura update ---> Plus d'id de dp dans l'url
    projectId = projectId.split("|")[1]
    # ParametersCheck
    if not projectUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    # TODO : check blocklevels

    # save blocklevels
    data_provider = data_provider_manager.get_single_data_provider("Python module Data Provider")
    
    try:
        data_provider.update_block_structure(projectId, blocklevels)
    except Exception as e:
        print(e)
        return "Something went wrong updating block structure", 500


    return blocklevels, 200


# Expected_results
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
    utils.updateJsonFile(
        dataPath + projectId + "/info.json", "resultStructure", resultStructure
    )
    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


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
    utils.updateJsonFile(
        dataPath + projectId + "/info.json", "resultStructure", resultStructure
    )

    # add to each results the default value
    for modelId in debiaiUtils.getModelsId(projectId):
        results = debiaiUtils.getModelResults(projectId, modelId)

        for key in results:
            results[key].append(resultColumn["default"])

        debiaiUtils.writeModelResults(projectId, modelId, results)

    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


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
    utils.updateJsonFile(
        dataPath + projectId + "/info.json", "resultStructure", resultStructure
    )

    # add to each results the default value
    for modelId in debiaiUtils.getModelsId(projectId):
        results = debiaiUtils.getModelResults(projectId, modelId)

        for key in results:
            results[key].pop(idx)

        debiaiUtils.writeModelResults(projectId, modelId, results)

    debiaiUtils.updateProject(projectId)
    return resultStructure, 200


def check_hash(projectId, data):
    if not debiaiUtils.projectExist(projectId):
        return "Project '" + projectId + "' doesn't exist", 404

    hash_list = data["hash_list"]

    hashmap = debiaiUtils.getHashmap(projectId)

    not_valide = []

    for hash in hash_list:
        if hash not in hashmap:
            not_valide.append(hash)

    return not_valide, 200
