import dataProviders.webDataProvider.http.api as api

from dataProviders.webDataProvider.useCases.models import get_models_info
from dataProviders.webDataProvider.useCases.selections import get_project_selections

from utils.utils import timeNow


def get_all_projects_from_data_provider(url, name):
    projects = api.get_projects(url)
    project_list = []

    if not projects:
        return

    for project_id in projects:
        if "nbSamples" not in projects[project_id]:
            projects[project_id]["nbSamples"] = None

        if "nbModels" not in projects[project_id]:
            projects[project_id]["nbModels"] = None

        if "nbSelections" not in projects[project_id]:
            projects[project_id]["nbSelections"] = None

        if "name" not in projects[project_id]:
            projects[project_id]["name"] = project_id

        project_list.append(
            {
                "id": project_id,
                "dataProvider": name,
                "name": projects[project_id]["name"],
                "nbModels": projects[project_id]["nbModels"],
                "nbSamples": projects[project_id]["nbSamples"],
                "nbSelections": projects[project_id]["nbSelections"],
                "creationDate": timeNow(),
                "updateDate": timeNow(),
                "nbRequests": 0,
                "nbTags": 0,
            }
        )

    return project_list


def get_single_project_from_data_provider(url, data_provider_name, id_project):
    project = api.get_project(url, id_project)
    blockInfo = format_collumns_project_overview(project)
    # TODO: prevent crash if no selections or models routes in data provider
    selections = get_project_selections(url, id_project)
    models = get_models_info(url, id_project)

    if "nbSamples" in project:
        nbSamples = project["nbSamples"]
    else:
        nbSamples = None

    # Converting views to DebiAI projects
    return {
        "id": id_project,
        "name": project["name"],
        "dataProvider": data_provider_name,
        "blockLevelInfo": blockInfo,
        "resultStructure": project["expectedResults"],
        "nbModels": len(models),
        "nbSamples": nbSamples,
        "nbRequests": 0,
        "nbTags": 0,
        "nbSelections": len(selections),
        "creationDate": timeNow(),
        "updateDate": timeNow(),
        "selections": selections,
        "models": models,
    }


def format_collumns_project_overview(project):
    try:
        otherColumns = []
        contextColumns = []
        annotationsColumns = []
        featuresColumns = []
        #
        #   Just removed old columns for category, need to take position with TOM on wich
        #   columns could stay or not
        #
        # Convert data columns to DebiAi structure
        for column in project["columns"]:
            debiaiColumn = {
                "name": column["name"],
                "type": column["type"] if "type" in column else "auto",
            }
            if "category" in column and column["category"] == "contexts":
                contextColumns.append(debiaiColumn)
            elif "category" in column and column["category"] == "annotations":
                annotationsColumns.append(debiaiColumn)
            elif "category" in column and column["category"] == "features":
                featuresColumns.append(debiaiColumn)
            else:
                otherColumns.append(debiaiColumn)

                # Final Debiai Structure for the project
        blockLevelInfo = [
            {
                "name": "Data Id",
                "others": otherColumns,
                "contexts": contextColumns,
                "features": featuresColumns,
                "annotations": annotationsColumns,
            }
        ]

        return blockLevelInfo
    except Exception as e:
        print(e)    
    
