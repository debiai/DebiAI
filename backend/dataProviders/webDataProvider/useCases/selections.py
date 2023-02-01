import dataProviders.webDataProvider.http.api as api
from utils.utils import timeNow


def get_project_selections(url, project_id):
    selections = api.get_selections(url, project_id)

    debiai_selections = []
    for selection in selections:
        selection_to_add = {
            "name": selection["name"] if "name" in selection else selection["id"],
            "id": selection["id"],
        }

        if "nbSamples" in selection:
            selection_to_add["nbSamples"] = selection["nbSamples"]
        if "creationDate" in selection:
            selection_to_add["creationDate"] = selection["creationDate"]
        if "updateDate" in selection:
            selection_to_add["updateDate"] = selection["updateDate"]

        debiai_selections.append(selection_to_add)
    return debiai_selections


def get_id_list_from_selection(url, project_id, selection_id):
    return api.get_selection_id(url, project_id, selection_id)


def create_selection(url, project_id, name, id_list, request_id):
    data = {"idList": id_list, "name": name}

    if request_id is not None:
        data["request"]: request_id

    return api.post_selection(url, project_id, data)


def delete_selection(url, project_id, selection_id):
    return api.delete_selection(url, project_id, selection_id)
