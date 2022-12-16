from dataProviders.DataProvider import DataProvider
from dataProviders.DataProviderException import DataProviderException
from utils.utils import get_app_version
from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils, projects, samples, selections, models, tree
PYTHON_DATA_PROVIDER_ID = "Python module Data Provider"


class PythonDataProvider(DataProvider):
    # Generic functions
    def __init__(self):
        pythonModuleUtils.init()
        print("  Python module Data Provider initialized")

    @property
    def name(self):
        return PYTHON_DATA_PROVIDER_ID

    def is_alive(self):
        return True

    def get_info(self):
        # Request method to get info on data Provider
        # return Object { version, dp_name, nb_Sample_max(to load)}
        # Get DebiAI version
        return {
            "version": get_app_version(),
            "dp_name": self.name,
        }

    # Projects
    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}]
        return projects.get_projects()

    def get_project(self, id):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}

        if not projects.project_exist(id):
            raise DataProviderException("Project not found", 404)

        project_base_info = projects.get_project(id)
        project_base_info["selections"] = selections.get_selections(id)
        project_base_info["resultStructure"] = projects.get_result_structure(id)
        project_base_info["models"] = models.get_models(id)
        return project_base_info

    # Id list
    def get_id_list(self, project_id, _from=None, _to=None):
        # Get id list
        # Return Arr[id]
        return samples.get_all_samples_id_list(project_id, _from, _to)

    def get_samples(self, project_id, id_list):
        # Get full data from id list
        # Return object { id: [data]}
        return samples.get_data_from_sampleid_list(project_id, id_list)

    # Selections
    def get_selections(self, project_id):
        # Get selections on project
        # Return arr[object{ id, name, creation_time, nb_samples}]
        return selections.get_selections(project_id)

    def get_selection_id_list(self, project_id, selection_id):
        # Get selections id for a project
        # Return selection ID list
        return selections.get_selection_id_list(project_id, selection_id)

    def create_selection(self, project_id, name, id_list, request_id=None):
        # Selection creation
        return selections.create_selection(project_id, name, id_list, request_id)

    def delete_selection(self, project_id, selection_id):
        # Selection deletion
        return selections.delete_selection(project_id, selection_id)

    # Models
    def get_models(self, project_id):
        return models.get_models(project_id)

    def get_model_results_id_list(self, project_id, model_id):
        return models.get_model_id_list(project_id, model_id)

    def get_model_results(self, project_id, model_id, id_list):
        return models.get_model_results(project_id, model_id, id_list)

    # Python module specific functions
    def delete_project(self, id):
        # Check if project exist
        if not projects.project_exist(id):
            raise DataProviderException("Project does not exist", 404)

        # Request method to delete project
        projects.delete_project(id)

    def create_project(self, name):
        # Check if project already exist
        if projects.project_exist(name):
            raise DataProviderException("Project already exists", 400)

        return projects.create_project(name, name)

    def update_block_structure(self, projectId, blockStructure):
        # Check if project exist
        if not projects.project_exist(projectId):
            raise DataProviderException("Project does not exist", 404)

        projects.update_block_structure(projectId, blockStructure)

    def add_block_tree(self, projectId, data):
        # Paramet ersCheck
        if not projects.project_exist(projectId):
            raise DataProviderException("Project does not exist", 404)
        
        return tree.add_block_tree(projectId, data)


    def update_results_structure(self, projectId, resultsStructure):
        # Check if project exist
        if not projects.project_exist(projectId):
            raise DataProviderException("Project does not exist", 404)

        # TODO : check resultStructure (type and default type ==)
        existing_result_structure = projects.get_result_structure(projectId)
        if existing_result_structure is not None:
            raise DataProviderException(
                "project " + projectId + " already have a results structure", 403)

        projects.update_results_structure(projectId, resultsStructure)

    def create_model(self, project_id, data):
        # Check if project exist
        if not projects.project_exist(project_id):
            raise DataProviderException("Project does not exist", 404)

        models.create_model(
            project_id,
            data["name"],
            data["metadata"] if "metadata" in data else None
        )

    def delete_model(self, project_id, model_id):
        models.create_model(project_id, model_id)

    def add_results_dict(self, project_id, model_id, data):
        models.add_results_dict(project_id, model_id, data)
