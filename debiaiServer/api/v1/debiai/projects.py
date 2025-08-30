#############################################################################
# Imports
#############################################################################
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
from debiaiServer.api.v1.exploration_statistics.utils import get_columns_statistics

#############################################################################
# PROJECTS Management
#############################################################################

# TODO LOIC : for API compatibilité, we do not change the registered method content
# TODO proposer 2 internal module : legacy (v1 implementation & 1 based on parquet)


def change_project_overview_v2(project_info, column_info):
    v2_project_info = {
        "id": project_info["id"],
        "name":  project_info["name"],
        "creationDate":  project_info["creationDate"],
        "updateDate":  project_info["updateDate"],
        "tags": [],
        "metadatas": {

        },
        "metrics": {
            "nbModels":  project_info["nbModels"],
            "nbSelections":  project_info["nbSelections"],
            "nbSamples":  project_info["nbSamples"],
        },
        "columns": column_info
        # projectColumns, get from statistic et supprimer doublon
        # "blockLevelInfo": projectBlockLevel, supprimer ici, garder dans l'API pour module python en V1
    }
    return v2_project_info


def get_projects():
    # Return a list of project overviews from all the data providers
    data_providers_list = data_provider_manager.get_data_provider_list()
    projectOverviews = []
    for data_provider in data_providers_list:
        try:
            projects = data_provider.get_projects()

            if projects is not None:
                # Adding data provider id to projects
                for project in projects:

                    stats = get_columns_statistics(data_provider.name,  project["id"])
                    project_inf = change_project_overview_v2(project, stats["columns"])
                    projectOverviews.append(project_inf)

                    if data_provider.name != "Python module Data Provider":
                        project_inf["dataProviderId"] = data_provider.name
                    else:
                        project_inf["dataProviderId"] = 'internal'

        except DataProviderException as e:
            print("Warning get DP projects : " + e.message)

    return projectOverviews, 200
