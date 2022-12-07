from abc import ABC, abstractmethod, abstractproperty


class DataProvider(ABC):
    
    @abstractproperty
    def name(self):
        pass
    
    @abstractproperty
    def is_alive(self):
        return False
    
    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_projects(self):
        pass

    @abstractmethod
    def get_project(self, id):
        pass

    # @abstractmethod
    # def delete_project(self, _id):
    #     pass

    @abstractmethod
    def get_id_list(self, _from, _to):
        pass

    @abstractmethod
    def get_samples(self, id_list):
        pass

    @abstractmethod
    def get_selections(self):
        pass

    @abstractmethod
    def get_selection_id_list(self, id):
        pass

    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def get_model_results_id_list(self):
        pass

    @abstractmethod
    def get_model_results(self, id_list):
        pass

