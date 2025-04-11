from fastapi import APIRouter, HTTPException
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager

router = APIRouter()

#############################################################################
# PROJECTS Management
#############################################################################


@router.get("/version", summary="Ping to check if the backend is running")
def ping():
    return {"status": "Online"}


@router.get("/projects", summary="Get the projects overview")
def get_projects():
    # Return a list of project overviews from all the data providers
    data_providers_list = data_provider_manager.get_data_provider_list()
    project_overviews = []
    for data_provider in data_providers_list:
        try:
            projects = data_provider.get_projects()
            if projects is not None:
                # Adding data provider id to projects
                for project in projects:
                    project["dataProviderId"] = data_provider.name
                project_overviews.extend(projects)
        except DataProviderException as e:
            print("Warning get DP projects: " + e.message)

    return project_overviews


@router.get(
    "/data-providers/{dataProviderId}/projects",
    summary="Get the projects overview for a data provider",
)
def get_data_providers_project(dataProviderId: str):
    # Return a list of project overviews for a specific data provider
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

    if data_provider is None:
        raise HTTPException(status_code=404, detail="Data provider not found")

    try:
        projects = data_provider.get_projects()
        if projects is not None:
            # Adding data provider id to projects
            for project in projects:
                project["dataProviderId"] = data_provider.name
        return projects
    except DataProviderException as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.message}")


@router.get(
    "/data-providers/{dataProviderId}/projects/{projectId}",
    summary="Get project details",
)
def get_project(dataProviderId: str, projectId: str):
    # Return the info about datasets, models, selections & tags
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        project = data_provider.get_project(projectId)
        # Adding data provider id to project
        project["dataProviderId"] = dataProviderId
        return project
    except DataProviderException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete(
    "/data-providers/{dataProviderId}/projects/{projectId}",
    summary="Delete a project",
)
def delete_project(dataProviderId: str, projectId: str):
    # Delete a project
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_provider.delete_project(projectId)
        return {"message": "Project deleted"}
    except DataProviderException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post(
    "/data-providers/{dataProviderId}/projects/{projectId}/dataIdList",
    summary="Get the project data id list",
)
def get_data_id_list(dataProviderId: str, projectId: str, requestParameters: dict):
    # Return the list of data ids
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data_id_list = data_provider.get_id_list(
            projectId,
            requestParameters["analysis"],
            requestParameters["from"],
            requestParameters["to"],
        )
        return data_id_list
    except DataProviderException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
