#############################################################################
# Imports
#############################################################################
import shutil
import ujson as json

import utils.utils as utils
import dataProviders.DataProviderException as DataProviderException
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

    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)

    try:
        project = data_provider.get_project(projectId)
        project["id"] = dataProviderId + "|" + project["id"]
        return project, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_project(data):
    # Ask a data provider to create a project
    dataProviderId = "Python module Data Provider" # TODO : deal with route
    projectName = data["projectName"]

    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)

    # Check project name
    if len(projectName) > 100:
        return "Project name too long", 400

    try:
        project = data_provider.create_project(projectName)
        project["id"] = dataProviderId + "|" + project["id"]
        return project, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def delete_project(projectId):
    # Delete a project
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]

    data_provider = data_provider_manager.get_single_data_provider(
        dataProviderId)

    try:
        data_provider.delete_project(projectId)
        return "Project deleted", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code



# def post_addExpectedResult(projectId, resultColumn):
#     # Add acolumn to the expecter results structure
#     # ParametersCheck
#     if not debiaiUtils.project_exist(projectId):
#         return "project " + projectId + " not found", 404

#     resultStructure = debiaiUtils.get_result_structure(projectId)

#     if resultStructure is None:
#         return "project " + projectId + " does not have a results structure", 403

#     # TODO : check resultStructure (type and default type ==)

#     resultStructure.append(resultColumn)

#     # save updated resultStructure
#     utils.updateJsonFile(
#         dataPath + projectId + "/info.json", "resultStructure", resultStructure
#     )

#     # add to each results the default value
#     for modelId in debiaiUtils.getModelsId(projectId):
#         results = debiaiUtils.getModelResults(projectId, modelId)

#         for key in results:
#             results[key].append(resultColumn["default"])

#         debiaiUtils.writeModelResults(projectId, modelId, results)

#     debiaiUtils.update_project(projectId)
#     return resultStructure, 200


# def delete_expectedResult(projectId, resultColumn):
#     # Add acolumn to the expecter results structure
#     # ParametersCheck
#     if not debiaiUtils.project_exist(projectId):
#         return "project " + projectId + " not found", 404

#     resultStructure = debiaiUtils.get_result_structure(projectId)

#     if resultStructure is None:
#         return "project " + projectId + " does not have a results structure", 403

#     # TODO : check resultStructure (type and default type ==)

#     length_results = len(resultStructure)
#     idx = -1
#     resultColumn = resultColumn["value"]

#     for i in range(length_results):
#         if resultStructure[i]["name"] == resultColumn:
#             resultStructure.pop(i)
#             idx = i
#             break

#     if idx == -1:
#         return "Columns " + resultColumn + " does not exists.", 404

#     # save updated resultStructure
#     utils.updateJsonFile(
#         dataPath + projectId + "/info.json", "resultStructure", resultStructure
#     )

#     # add to each results the default value
#     for modelId in debiaiUtils.getModelsId(projectId):
#         results = debiaiUtils.getModelResults(projectId, modelId)

#         for key in results:
#             results[key].pop(idx)

#         debiaiUtils.writeModelResults(projectId, modelId, results)

#     debiaiUtils.update_project(projectId)
#     return resultStructure, 200


# def check_hash(projectId, data):
#     if not debiaiUtils.project_exist(projectId):
#         return "Project '" + projectId + "' doesn't exist", 404

#     hash_list = data["hash_list"]

#     hashmap = debiaiUtils.getHashmap(projectId)

#     not_valide = []

#     for hash in hash_list:
#         if hash not in hashmap:
#             not_valide.append(hash)

#     return not_valide, 200
