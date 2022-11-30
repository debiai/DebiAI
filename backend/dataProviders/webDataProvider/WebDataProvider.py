from dataProviders.DataProvider import DataProvider

class WebDataProvider(DataProvider):
    def _init_(self, url, name):
        self.url = url
        self.name = name
        
    def get_info(self):
        # Request method to get info on data Provider
        # return Object { version, dp_name, nb_Sample_max(to load), can_delete?}
        pass
        
    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}] 
        pass
    
    
    def get_project(self, id):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}
        pass
    
    
    # def delete_project(self, _id):
    #     # Request method to delete project
    #     pass
    
    
    def get_id_list(self, project_id, _from=None, _to=None):
        # http Request on dp to get id list
        # Return Arr[id]
        pass
    
    
    def get_samples(self, project_id, id_list):
        # http Request get full sample
        # Return object { id: [data]}
        pass


    def get_selections(self, project_id, id_list):
        # Get selections on project
        # Return arr[object{ id, name, creation_time, nb_samples}]
        pass

    
    def get_selection(self, project_id, selection_id):
        # Get selections id for a project
        # 
        pass
    
    
    def get_models(self, project_id):
        pass
    
    
    def get_model_results(self, id_list):
        pass
    
    
    