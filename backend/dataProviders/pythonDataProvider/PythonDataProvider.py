from dataProviders.DataProvider import DataProvider
from utils.utils import utils as GlobalUtils
import dataUtils.utils as utils
import dataUtils.projects as projects
import dataUtils.samples as samples
import dataUtils.selections as selections
import dataUtils.models as models


class PythonDataProvider(DataProvider):
    def _init_(self):
        utils.init()

    def get_info(self):
        # Request method to get info on data Provider
        # return Object { version, dp_name, nb_Sample_max(to load)}
        # Get DebiAI version
        return {
            "version": GlobalUtils.get_version(),
            "dp_name": "Python module Data Provider",
        }

    def get_projects(self):
        # Request method to get projects overview
        # Return Arr[object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}]
        return projects.get_projects()

    def get_project(self, id):
        # Request method to get projects overview
        # Return object{ id, name, nb_samples, nb_models, nb_selections, update_time, creation_time}
        return projects.getProjectOverview(id)

    def delete_project(self, id):
        # Request method to delete project
        projects.deleteProject(id)

    def get_id_list(self, project_id, _from=None, _to=None):
        # http Request on dp to get id list
        # Return Arr[id]
        return samples.get_list(project_id, {"from": _from, "to": _to}).samples

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

    def get_model_results(self,project_id, model_id, id_list):
        return models.getModelResults(project_id, model_id, id_list)
