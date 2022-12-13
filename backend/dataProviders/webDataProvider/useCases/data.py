from dataProviders.webDataProvider.http.api import get_id_list, get_samples


#
# UseCase folder role is the middleware between class methods and http requests
# It's used to make all changes in data we took from DP and send it back to the class/controller
#

def get_project_id_list(url, id_project, _from=None, _to=None):
    id_list = get_id_list(url, id_project, _from, _to)
    
    return id_list

def get_project_samples(url,id_project, id_list):
    
    data = get_samples(url, id_project, id_list)
    
    return data