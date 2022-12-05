from dataProviders.webDataProvider.http.api import (
    get_projects,
    get_project,
    get_selections,
    get_models,
)
from utils.utils import timeNow

def get_all_projects_from_data_provider(url, name):
    projects = get_projects(url)
    project_list = []
        
    for project in projects:
        blockInfo = format_collumns_project_overview(projects[project])
        selections = format_selections_project_overview(url, project)
        models = format_models_for_overview(url, project)
        # Samples number
        if "nbSamples" in projects[project]:
            nbSamples = projects[project]["nbSamples"]
        else:
            nbSamples = None
            
        project_list.append({
            "id": name + "|" + project,
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
    print(project)
    #### Todo : remove when data Provider API will be changed 
    project = project[id_project]
    print("=================== project selected =====================")
    print(project)
    blockInfo = format_collumns_project_overview(project)
    selections = format_selections_project_overview(url, project)
    models = format_models_for_overview(url, project)
    
    if "nbSamples" in project:
        nbSamples = project["nbSamples"]
    else:
        nbSamples = None

    # Converting views to DebiAI projects
    return {
        "id": data_provider_name + "|" + id_project,
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

def format_selections_project_overview(url, id_project):
    # Get selections for the project
    selections = get_selections(url, id_project)
    
    debiai_selections = []
    for selection in selections:
        debiai_selections.append(
            {
                "name": selection["name"] if "name" in selection else selection["id"],
                "id": selection["id"],
                "nbSamples": selection["nbSamples"] if "nbSamples" in selection else 0,
                "creationDate": timeNow(),
                "updateDate": timeNow(),
            }
        )
    return debiai_selections

def format_models_for_overview(url, id_project):
    # Models
    models = get_models(url, id_project)
    debiai_models = []
    for model in models:
        debiai_models.append(
            {
                "name": model["name"] if "name" in model else model["id"],
                "id": model["id"],
                "nbResults": model["nbResults"] if "nbResults" in model else 0,
                "creationDate": timeNow(),
                "updateDate": timeNow(),
                "metadata": {},
            }
        )
    
    return debiai_models    
