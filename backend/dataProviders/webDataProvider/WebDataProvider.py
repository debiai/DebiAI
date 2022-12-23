from dataProviders.DataProvider import DataProvider
from dataProviders.webDataProvider.useCases.data import get_project_id_list, get_project_samples
from dataProviders.webDataProvider.useCases.projects import get_all_projects_from_data_provider, get_single_project_from_data_provider
from dataProviders.webDataProvider.useCases.models import get_model_results, get_models_info, get_model_result_id
from dataProviders.webDataProvider.useCases.selections import get_project_selections, get_id_list_from_selection
from dataProviders.webDataProvider.http.api import get_info, is_alive

from dataProviders.DataProviderException import DataProviderException


#
# Class role is supposed to expose methods for every data Providers
#
#
class WebDataProvider(DataProvider):
    def __init__(self, url, name):
        self.url = url
        self._name = name

    @property
    def name(self):
        return self._name
    
    ## Todo api call Info (new info)
    def is_alive(self):
        return is_alive(self.url)

    def get_info(self):
        return get_info(self.url)

    ### API OK
    ### USE CASE OK
    ### CONTROLLER OK
    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}]
        return get_all_projects_from_data_provider(self.url, self.name)

    def get_project(self, id_project):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}
        return get_single_project_from_data_provider(self.url, self.name, id_project)


    def delete_project(self, project_id):
        raise DataProviderException("Deleting a project is not supported by this data provider", 400)


    ### API OK
    ### USE CASE OK
    ### CONTROLLER -> NOK
    def get_id_list(self, project_id, _from=None, _to=None):
        # http Request on dp to get id list
        # Return Arr[id]
        return get_project_id_list(self.url, project_id, _from, _to)
        

    def get_samples(self, project_id, id_list):
        # http Request get full sample
        # Return object { id: [data]}
        return get_project_samples(self.url, project_id, id_list)
    
    
    ### API NOK
    ### USE CASE NOK
    ### CONTROLLER -> NOK
    def get_selections(self, project_id):
        # Get selections on project
        # Return arr[object{ id, name, creation_time, nb_samples}]
        return get_project_selections(self.url, project_id)
    
    def get_selection_id_list(self, project_id, selection_id):
        return get_id_list_from_selection(self.url, project_id, selection_id)

    def create_selection(self, name, id_list):
        raise DataProviderException("Not implemented yet", 400) # TODO

    def delete_selection(self, project_id, selection_id):
        raise DataProviderException("Deleting a selection is not supported by this data provider", 400)

    ### API OK
    ### USE CASE OK
    ### CONTROLLER -> NOK
    def get_models(self, project_id):        
        return get_models_info(self.url, project_id)
    
    
    def get_model_results_id_list(self, project_id, model_id):
        return get_model_result_id(self.url, project_id, model_id)

    def get_model_results(self, project_id, model_id, sample_list):
        return get_model_results(self.url, project_id, model_id, sample_list)

    def delete_model(self, project_id, model_id):
        raise DataProviderException("Deleting a model is not supported by this data provider", 400)