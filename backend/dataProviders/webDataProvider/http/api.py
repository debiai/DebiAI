import requests

def get_info(url):
    try:
        r = requests.get(url + 'info')
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def get_projects(url):
    try:
        r = requests.get(url + '/projects')
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None
    
def get_project(url, id_project):
    try:
        r = requests.get(url + '/projects/' + id_project)
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None
    
def get_id_list(url, id_project, _from, _to):
    try:
        r = requests.get(url + '/projects/' + id_project + '/data-id-list')
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print("Error getting data id list from {} on view {}".format(
                url, id_project))
        return []
    
def get_samples(url, id_project, id_list):
    try:
        r = requests.post(
            url + "projects/{}/data".format(id_project), json=id_list)
        return r.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise Exception(
            "Could not get the data provider {} data for view {}".format(url, id_project))
        
def get_selections(url, id_project):
    try:
        r = requests.get(url + "projects/{}/selections".format(id_project))
        return r.json() 
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def get_selection(url, id_project, id_selection):
    try:
        r = requests.get(url + "projects/{}/selections/{}".format(id_project, id_selection))
        return r.json() 
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None
    
def get_models(url, id_project):
    try:
        r = requests.get(url + "projects/{}/models".format(id_project))
        return r.json() 
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

    
def get_model_result(url, id_project, id_model, id_sample_list):
    try:
        r = requests.post(url + "projects/{}/models/{}/results".format(id_project, id_model), json=id_sample_list)
        return r.json() 
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None