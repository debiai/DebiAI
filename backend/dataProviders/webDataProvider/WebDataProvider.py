from dataProviders.DataProvider import DataProvider
from dataProviders.webDataProvider.useCases.data import get_project_id_list, get_project_samples
from dataProviders.webDataProvider.useCases.projects import get_all_projects_from_data_provider, get_single_project_from_data_provider
from dataProviders.webDataProvider.http.api import get_info
from dataProviders.webDataProvider.useCases.models import get_model_results, get_models_info



#
# Class role is supposed to expose methods for every data Providers
#
#
class WebDataProvider(DataProvider):
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def get_info(self):
        return get_info(self.url)

    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}]
        return get_all_projects_from_data_provider(self.url, self.name)

    def get_project(self, id_project):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}
        return get_single_project_from_data_provider(self.url, self.name, id_project)

    # def delete_project(self, _id):
    #     # Request method to delete project
    #     pass

    def get_id_list(self, project_id, _from=None, _to=None):
        # http Request on dp to get id list
        # Return Arr[id]
        return get_project_id_list(self.url, project_id, _from, _to)
        

    def get_samples(self, project_id, id_list):
        # http Request get full sample
        # Return object { id: [data]}
        return get_project_samples(self.url, project_id, id_list)
    
    
    def get_selections(self, project_id, id_list):
        # Get selections on project
        # Return arr[object{ id, name, creation_time, nb_samples}]
        pass

    def get_selection(self, project_id, selection_id):
        # Get selections id for a project
        #
        pass

    def get_models(self, project_id):        
        return get_models_info(self.url, project_id)
    

    def get_model_results(self, project_id, model_id, sample_list):
        return get_model_results(self.url, project_id, model_id, sample_list)
