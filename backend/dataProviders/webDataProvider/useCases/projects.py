from backend.dataProviders.webDataProvider.http.api import get_projects, get_project, get_selections, get_models
from utils.utils import timeNow



def get_all_projects_from_data_provider(url):
    projects = get_projects(url)
    
    ###### Modify rest of function with what we need
    return projects

def get_single_project_from_data_provider(url, id_project):
    project = get_project(url, id_project)
    
    otherColumns = []
    contextColumns = []
    groundTruthColumns = []
    inputColumns = []
    
    # Convert data columns to DebiAi structure
    for column in project["columns"]:
        debiaiColumn = {
            "name": column["name"],
            "type": column["type"] if "type" in column else "auto"
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
    blockLevelInfo = [{
        "name": "Data Id",
        "others": otherColumns,
        "contexts": contextColumns,
        "groundTruth": groundTruthColumns,
        "inputs": inputColumns
    }]
    
    
    # Samples number
    if "nbSamples" in project:
        nbSamples = project["nbSamples"]
    else:
        nbSamples = None
        
    # Get selections for the project
    selections = get_selections(url, id_project)
    debiai_selections = []
    for selection in selections:
        debiai_selections.append({
            "name": selection["name"] if "name" in selection else selection["id"],
            "id": selection["id"],
            "nbSamples": selection["nbSamples"] if "nbSamples" in selection else 0,
            "creationDate": timeNow(),
            "updateDate": timeNow(),
        })
        
    # Models 
    models = get_models(url, id_project)
    debiai_models = []
    for model in models:
        debiai_models.append({
            "name": model["name"] if "name" in model else model["id"],
            "id": model["id"],
            "nbResults": model["nbResults"] if "nbResults" in model else 0,
            "creationDate": timeNow(),
            "updateDate": timeNow(),
            "metadata": {}
        })
        # Converting views to DebiAI projects
        return {
            "id": data_provider.name + "|" + view,
            "name": project["name"] | id_project,
            "dataProvider": data_provider.name,
            "view": id_project,
            "blockLevelInfo": blockLevelInfo,
            "resultStructure": project["expectedResults"],
            "nbModels": len(debiai_models),
            "nbSamples": nbSamples,
            "nbRequests": 0,
            "nbTags": 0,
            "nbSelections": len(selections),
            "creationDate": timeNow(),
            "updateDate": timeNow(),
            "modelOverviews": [],
            "selections": debiai_selections,
            "models": debiai_models,
        }
    

