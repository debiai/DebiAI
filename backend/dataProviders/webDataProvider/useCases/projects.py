from dataProviders.webDataProvider.http.api import (
    get_projects,
    get_project,
    get_selections,
)

from dataProviders.webDataProvider.useCases.models import get_models_info
from dataProviders.webDataProvider.useCases.selections import get_project_selections 

from utils.utils import timeNow

def get_all_projects_from_data_provider(url, name):
    projects = get_projects(url)
    project_list = []
        
    if not projects:
        return
    
    for project in projects:
        blockInfo = format_collumns_project_overview(projects[project])
        selections = get_project_selections(url, project)
        models = get_models_info(url, project)
        # Samples number
        if "nbSamples" in projects[project]:
            nbSamples = projects[project]["nbSamples"]
        else:
            nbSamples = None
            
        project_list.append({
            "id": project,
            "name": project,
            "dataProvider": name,
            "view": project,
            "blockLevelInfo": blockInfo,
            "resultStructure": projects[project]["expectedResults"],
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
        })
        
        
    ###### Modify rest of function with what we need
    return project_list


def get_single_project_from_data_provider(url, data_provider_name, id_project):
    project = get_project(url, id_project)
    #### Todo : remove when data Provider API will be changed
    project = project[id_project]
    blockInfo = format_collumns_project_overview(project)
    selections = get_selections(url, id_project)
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

