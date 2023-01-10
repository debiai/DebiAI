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

    try:
        project = data_provider.get_project(projectId)
        project["id"] = dataProviderId + "|" + project["id"]
        return project, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_project(data):
    # Ask a data provider to create a project
    dataProviderId = "Python module Data Provider"  # TODO : deal with route
    projectName = data["projectName"]

    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

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

    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    try:
        data_provider.delete_project(projectId)
        return "Project deleted", 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
