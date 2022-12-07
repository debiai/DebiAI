import requests


def is_alive(url):
    try:
        r = requests.get(url + '/ping')
        return r.status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def get_info(url):
    try:
        r = requests.get(url + "/info")
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

#### Info will be /projects when refactor will be done
def get_projects(url):
    try:
        r = requests.get(url + "/info")
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

#######  Info will be /projects/projectId when refactor will be done
def get_project(url, id_project):
    try:
        r = requests.get(url + "/info")
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None


def get_id_list(url, id_project, _from=None, _to=None):
    try:
        if _from is not None and _to is not None:
            url = url + "/projects/" + id_project + "/data-id-list"    
        else:     
            url = url + "/projects/" + id_project + "/data-id-list?from={}&to={}".format(_from, _to)
            
        r = requests.get(url)
            
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Error getting data id list from {} on view {}".format(url, id_project))
        return []


def get_samples(url, id_project, id_list):
    try:
        r = requests.post(url + "/projects/{}/data".format(id_project), json=id_list)
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise Exception(
            "Could not get the data provider {} data for view {}".format(
                url, id_project
            )
        )


def get_selections(url, id_project):
    try:
        r = requests.get(url + "/view/{}/selections".format(id_project))
        print(r)
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None


def get_selection_id(url, id_project, id_selection):
    try:
        r = requests.get(
            url + "/projects/{}/selections/{}".format(id_project, id_selection)
        )
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None


def get_models(url, id_project):
    try:
        r = requests.get(url + "/view/{}/models".format(id_project))
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def get_model_result_id_list(url, project_id, model_id):
    try:
        r = requests.get(url + "/projects/{}/models/{}".format(project_id, model_id))
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def get_model_result(url, id_project, id_model, id_sample_list):
    try:
        r = requests.post(
            url + "/projects/{}/models/{}/results".format(id_project, id_model),
            json=id_sample_list,
        )
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None
