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

        if "nbSamples" in projects[project_id]:
            nbSamples = projects[project_id]["nbSamples"]
        else:
            nbSamples = None

        project_list.append(
            {
                "id": project_id,
                "name": (
                    project_id
                    if "name" not in projects[project_id]
                    else projects[project_id]["name"]
                ),
                "dataProvider": name,
                "view": project_id,
                "nbModels": projects[project_id]["nbModels"],
                "nbSamples": nbSamples,
                "nbRequests": 0,
                "nbTags": 0,
                "nbSelections": projects[project_id]["nbSelections"],
                "creationDate": timeNow(),
                "updateDate": timeNow(),
                "modelOverviews": [],
            }
        )

    return project_list


def get_single_project_from_data_provider(url, data_provider_name, id_project):
    project = api.get_project(url, id_project)

    blockInfo = format_collumns_project_overview(project)
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
        "view": id_project,
        "blockLevelInfo": blockInfo,
        "resultStructure": project["expectedResults"],
        "nbModels": len(models),
        "nbSamples": nbSamples,
        "nbRequests": 0,
        "nbTags": 0,
        "nbSelections": len(selections),
        "creationDate": timeNow(),
        "updateDate": timeNow(),
        "modelOverviews": [],
        "selections": selections,
        "models": models,
    }


def format_collumns_project_overview(project):
    otherColumns = []
    contextColumns = []
    groundTruthColumns = []
    inputColumns = []

    # Convert data columns to DebiAi structure
    for column in project["columns"]:
        debiaiColumn = {
            "name": column["name"],
            "type": column["type"] if "type" in column else "auto",
        }
        if "category" in column and column["category"] == "context":
            contextColumns.append(debiaiColumn)
        elif "category" in column and column["category"] == "groundtruth":
            groundTruthColumns.append(debiaiColumn)
        elif "category" in column and column["category"] == "input":
            groundTruthColumns.append(debiaiColumn)
        else:
            otherColumns.append(debiaiColumn)

            # Final Debiai Structure for the project
    blockLevelInfo = [
        {
            "name": "Data Id",
            "others": otherColumns,
            "contexts": contextColumns,
            "groundTruth": groundTruthColumns,
            "inputs": inputColumns,
        }
    ]

    return blockLevelInfo
