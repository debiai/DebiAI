#############################################################################
# Imports
#############################################################################
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
import debiaiServer.modules.exportMethods.exportUtils as exportUtils
from debiaiServer.api.v1.exploration_statistics.utils import get_columns_statistics

#############################################################################
# Internal Data Provider
#############################################################################

dataProviderId = "json_block"


def get_data_providers_project():

    # Return a list of project overviews for a specific data provider
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    if data_provider is None:
        return "Data provider not found", 404

    try:
        projects = data_provider.get_projects()

        if projects is not None:
            # Adding data provider id to projects
            for project in projects:
                project["dataProviderId"] = data_provider.name

    except DataProviderException as e:
        print("Warning get DP projects : " + e.message)

    return projects, 200


def change_project_v1(project_info, column_info):
    v1_project_info = {
        "id": project_info["id"],
        "name": project_info["name"],
        "creationDate": project_info["creationDate"],
        "updateDate": project_info["updateDate"],
        "tags": [],
        "metadata": {},
        "metrics": {
            "nbModels": project_info["nbModels"],
            "nbSelections": project_info["nbSelections"],
            "nbSamples": project_info["nbSamples"],
        },
        "columns": column_info,
        # "nbModels": project_info["nbModels"],
        # "nbSelections": project_info["nbSelections"],
        # "nbSamples": project_info["nbSamples"],
        # "blockLevelInfo": project_info["blockLevelInfo"],
        "selections": project_info["selections"],
        "models": project_info["models"],
        # projectColumns, get from statistics and remove duplicates
        # "blockLevelInfo": projectBlockLevel, remove here, keep in the API for python module in V1
    }

    return v1_project_info


def get_project(projectId):
    # return the info about datasets, models, selections & tags
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        project = data_provider.get_project(projectId)

        stats = get_columns_statistics(data_provider.name, project["id"])
        project_inf = change_project_v1(project, stats["columns"])

        # Adding data provider id to project
        project_inf["dataProviderId"] = dataProviderId

        return project_inf, 200
    except DataProviderException as e:
        return e.message, e.status_code


def delete_project(projectId):
    # Delete a project
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        data_provider.delete_project(projectId)
        return "Project deleted", 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_data_id_list(projectId, requestParameters):
    # return the list of data ids
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        data_id_list = data_provider.get_id_list(
            projectId,
            requestParameters["analysis"],
            requestParameters["from"],
            requestParameters["to"],
        )

        return data_id_list, 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_model_id_list(projectId, modelId):
    """
    Get the list of models for a project
    """
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return list(data_provider.get_model_results_id_list(projectId, modelId)), 200
    except DataProviderException as e:
        return e.message, e.status_code


def delete_model(projectId, modelId):
    """
    Delete a model
    """
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.delete_model(projectId, modelId), 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_results(projectId, modelId, data):
    """
    Get the model results from a sample list
    """
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return (
            data_provider.get_model_results(projectId, modelId, data["sampleIds"]),
            200,
        )
    except DataProviderException as e:
        return e.message, e.status_code


def get_data(projectId, data):
    # return a project data from a list of ids
    sampleIds = data["sampleIds"]
    analysis = data["analysis"] if "analysis" in data else None

    try:
        # Find the data provider
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        # Ask for the data
        samples = data_provider.get_samples(projectId, analysis, sampleIds)

        if samples is not None:
            return {
                "data": samples,
                "dataMap": True,
            }, 200

        return (
            "Can't find samples for project "
            + projectId
            + " on data provider : "
            + dataProviderId,
            404,
        )
    except DataProviderException as e:
        return e.message, e.status_code


def get_selections(projectId):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.get_selections(projectId), 200
    except DataProviderException as e:
        return e.message, e.status_code


def post_selection(projectId, data):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        new_selection = data_provider.create_selection(
            projectId,
            data["selectionName"],
            data["sampleHashList"],
        )
        return new_selection, 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_selection_id_list(projectId, selectionId):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        return data_provider.get_selection_id_list(projectId, selectionId), 200
    except DataProviderException as e:
        return e.message, e.status_code


def delete_selection(projectId, selectionId):
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.delete_selection(projectId, selectionId)
        return "Selection deleted", 200
    except DataProviderException as e:
        return e.message, e.status_code


def exportSelection(dataProviderId, projectId, data):
    try:
        return exportUtils.exportSelection(dataProviderId, projectId, data), 200
    except Exception as e:
        return str(e), 400
