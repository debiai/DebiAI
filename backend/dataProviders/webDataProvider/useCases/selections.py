from dataProviders.webDataProvider.http.api import get_selections, get_selection_id, post_selection
from utils.utils import timeNow


def get_project_selections(url, project_id):
    selections = get_selections(url, project_id)
    
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
    


def get_id_list_from_selection(url, project_id, selection_id):
    return get_selection_id(url, project_id, selection_id)


def create_selection(url, project_id, name, id_list, request_id):
    
    data = {
        "idList": id_list,
        "name": name
    }
    
    if request_id is not None:
        data["request"]: request_id
        
    return post_selection(url, project_id, data)

