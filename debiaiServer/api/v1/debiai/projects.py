#############################################################################
# Imports
#############################################################################
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
from debiaiServer.api.v1.debiai.utils import make_hash

#############################################################################
# PROJECTS Management
#############################################################################


def change_project_overview_v1(project_info):
    v1_project_info = {
        "id": project_info["id"],
        "dataProviderProjectId": project_info["id"],  # same id for test
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
        # "columns": column_info,
        # projectColumns, get from statistic et suppress
        # "blockLevelInfo": projectBlockLevel, suppress here keep
    }
    return v1_project_info


def get_projects(prev_hash_content=None):
    # Return a list of project overviews from all the data providers
    data_providers_list = data_provider_manager.get_data_provider_list()
    projectOverviews = {}
    projectList = []
    print("data_provider Get projects")
    for data_provider in data_providers_list:
        print(data_provider)
        try:
            projects = data_provider.get_projects()

            if projects is not None:
                # Adding data provider id to projects
                for project in projects:
                    project_inf = change_project_overview_v1(project)
                    projectList.append(project_inf)

                    if data_provider.name != "Python module Data Provider":
                        project_inf["dataProviderId"] = data_provider.name
                    else:
                        project_inf["dataProviderId"] = "json_block"

        except DataProviderException as e:
            print("Warning get DP projects : " + e.message)

    new_hash = "prj_" + str(
        +make_hash(projectList)
    )  # We add a prefix to avoir empty string

    print(
        new_hash,
        " <=> ",
        prev_hash_content,
        type(new_hash),
        type(prev_hash_content),
        new_hash == prev_hash_content,
    )
    if new_hash == prev_hash_content:
        return None, 304
    else:
        projectOverviews["projects"] = projectList
        projectOverviews["hash_content"] = new_hash
        return projectOverviews, 200
