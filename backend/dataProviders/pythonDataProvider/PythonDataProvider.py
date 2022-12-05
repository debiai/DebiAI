from dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils
from dataProviders.DataProvider import DataProvider
from utils.utils import get_app_version
from dataProviders.pythonDataProvider.dataUtils import projects, samples, selections, models

PYTHON_DATA_PROVIDER_ID = "Python module Data Provider"


class PythonDataProvider(DataProvider):
    def __init__(self):
        pythonModuleUtils.init()
        self.name = PYTHON_DATA_PROVIDER_ID
        print("  Python module Data Provider initialized")

    def get_info(self):
        # Request method to get info on data Provider
        # return Object { version, dp_name, nb_Sample_max(to load)}
        # Get DebiAI version
        return {
            "version": get_app_version(),
            "dp_name": self.name,
        }

    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}]
        return projects.get_projects()

    def get_project(self, id):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}
        project_base_info = projects.get_project(id)
        project_base_info["selections"] = selections.get_selections(id)
        project_base_info["models"] = models.get_models(id)
        return project_base_info

    def delete_project(self, id):
        # Request method to delete project
        projects.deleteProject(id)

    def get_id_list(self, project_id, _from=None, _to=None):
        # http Request on dp to get id list
        # Return Arr[id]
        return samples.get_all_samples_id_list(project_id, _from, _to)

    def get_samples(self, project_id, id_list):
        # http Request get full sample
        # Return object { id: [data]}
        return samples.get_data_from_sampleid_list(project_id, id_list)

    def get_selections(self, project_id):
        # Get selections on project
        # Return arr[object{ id, name, creation_time, nb_samples}]
        return selections.get_selections(project_id)

    def get_selection_id_list(self, project_id, selection_id):
        # Get selections id for a project
        # Return selection ID list
        return selections.getSelectionSamples(project_id, selection_id)

    def get_models(self, project_id):
        return models.getModels(project_id)

    def get_model_results(self, project_id, model_id, id_list):
        return models.getModelResults(project_id, model_id, id_list)
