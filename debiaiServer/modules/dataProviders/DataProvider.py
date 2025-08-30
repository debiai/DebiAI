from abc import ABC, abstractmethod


class DataProvider(ABC):
    # Data
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def is_alive(self):
        return False

    @property
    @abstractmethod
    def type(self):
        pass

    #  Differentiate Name and ID => Use ID for the request, as Name is more free content
    @property
    @abstractmethod
    def id(self):
        pass

    # Info
    @abstractmethod
    def get_info(self) -> dict:
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

    def supports_project_id(self, project_id):
        """
        Check if the data provider supports the given project ID.
        This can be overridden by specific data providers if needed.

        This function was made for the exploration compatibility.
        Avoid using it in other contexts unless necessary.
        """
        projects = self.get_projects()
        if not projects:
            return False
        return any(project["id"] == project_id for project in projects)
