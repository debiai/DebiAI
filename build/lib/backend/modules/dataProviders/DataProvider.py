from abc import ABC, abstractmethod, abstractproperty


class DataProvider(ABC):
    # Data
    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def is_alive(self):
        return False

    @abstractproperty
    def type(self):
        pass

    # Info
    @abstractmethod
    def get_info(self):
        pass

    # Projects
    @abstractmethod
    def get_projects(self):
        pass

    @abstractmethod
    def get_project(self, id):
        pass

    @abstractmethod
    def delete_project(self, _id):
        pass

    # Samples
    @abstractmethod
    def get_id_list(self, _projectId, _analysis, _from, _to):
        pass

    @abstractmethod
    def get_samples(self, _projectId, _analysis, id_list):
        pass

    # Selections
    @abstractmethod
    def get_selections(self):
        pass

    @abstractmethod
    def get_selection_id_list(self, id):
        pass

    @abstractmethod
    def create_selection(self, name, id_list):
        pass

    @abstractmethod
    def delete_selection(self, id):
        pass

    # Models
    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def get_model_results_id_list(self):
        pass

    @abstractmethod
    def get_model_results(self, id_list):
        pass

    @abstractmethod
    def delete_model(self, id):
        pass
