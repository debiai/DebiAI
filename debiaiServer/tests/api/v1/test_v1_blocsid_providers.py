import requests
import ujson as json
import pytest

appUrl = "http://localhost:3000/api/v1/"

# Creation of the DEBIAI wine quality project block structure
DEBIAI_block_structure = [
    {
        "name": "sampleId",
        "inputs": [
            {"name": "input_1",        "type": "number"},
            {"name": "input_2",        "type": "text"},
        ],
        "groundTruth": [
            {"name": "quality",         "type": "number"},
        ]
    }
]

DEBIAI_basic_block = {
    "blockTree": [
        {"name": "0", "inputs": [25, "test"], "groundTruth": [0.25]},
        {"name": "1", "inputs": [12, "debug"], "groundTruth": [0.82]},
        {"name": "2", "inputs": [47, "toto"], "groundTruth": [-2]},
        {"name": "3", "inputs": [99, "tata"], "groundTruth": [0.2]}
    ]
 }


class TestBlocsIdProvider:

    PYTHON_DATA_PROVIDER_ID: str = "Python module Data Provider"
    PYTHON_API_URL: str = "http://localhost:3000/api/v0/"
    PROJECT_NAME_1: str = "Block ID Default Project"

    def delete_project(self, project_name, fail_if_not_found: bool = False):

        url = (self.PYTHON_API_URL + "data-providers/" + self.PYTHON_DATA_PROVIDER_ID + "/projects/" + project_name)
        resp = requests.request("DELETE", url, headers={}, data={})
        if fail_if_not_found:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 200 or resp.status_code == 404

    def create_project(self, project_name):
        url = self.PYTHON_API_URL + "projects"
        resp = requests.post(url=url, headers={}, json={"projectName": project_name})
        assert resp.status_code == 200

        # Get Id # WE DON NOT TEST THE API so we take as grand that good value are return for project ID
        data = json.loads(resp.text)
        test_project_id = data["id"]

        return test_project_id

    def create_blocklevels(self, project_name):

        url = self.PYTHON_API_URL + "data-providers/" + self.PYTHON_DATA_PROVIDER_ID + "/projects/" + project_name + "/blocklevels"  # noqa: E501
        resp = requests.post(url=url, headers={}, json=DEBIAI_block_structure, verify=False)
        assert resp.status_code == 200

    def add_project_data(self, project_name):
        url = self.PYTHON_API_URL + "data-providers/" + self.PYTHON_DATA_PROVIDER_ID + "/projects/" + project_name + "/blocks"  # noqa: E501
        resp = requests.post(url=url, headers={}, json=DEBIAI_basic_block, verify=False)
        assert resp.status_code == 200

    def get_project(self, project_name):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        return load

    @pytest.fixture
    def project_one(self):
        print('\nProjects one initiatization')

        # We reset project one if already exist
        self.delete_project(self.PROJECT_NAME_1)

        # create project one
        self.prj_one = self.create_project(self.PROJECT_NAME_1)
        self.create_blocklevels(self.PROJECT_NAME_1)
        self.add_project_data(self.PROJECT_NAME_1)
        yield
        print('\nProject init cleaning')

        # We reset project one if already exist
        # self.delete_project(self.prj_one)
        # delete if exists

    def test_get_data_ids(self, project_one):
        pass

    def otest_get_projects_check_project_one_empty(self, project_one):

        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200, "As no hass provider we shall have 200 response code"
        load = json.loads(resp.text)
        print(load)
        assert "projects" in load,  "We check projects are in the payload"

        project_list = load["projects"]
        assert len(project_list) == 1, "We check only one project exist"

        project_one = project_list[0]
        assert project_one['id'] == self.PROJECT_NAME_1, "We check The project name"

        # We chek project expected properties
        assert "name"           in project_one, "We check name  are in the projects payload"  # noqa:E272
        assert "updateDate"     in project_one, "We check creationDate  are in the projects payload"  # noqa:E272
        assert "creationDate"   in project_one, "We check creationDate  are in the projects payload"  # noqa:E272
        assert "dataProviderId" in project_one, "We check dataProviderId  are in the projects payload"  # noqa:E272
        assert "tags"           in project_one, "We check tags  are in the projects payload"  # noqa:E272
        assert "metadatas"      in project_one, "We check matadatas  are in the projects payload"  # noqa:E272
        assert "metrics"        in project_one, "We check metrics  are in the projects payload"  # noqa:E272
        assert "columns"        in project_one, "We check columns  are in the projects payload"  # noqa:E272

        # We chek mandatory metrics
        assert "nbModels"       in project_one['metrics'], "We check nbModels metrics is available"  # noqa:E272
        assert "nbSamples"      in project_one['metrics'], "We check nbModels metrics is available"  # noqa:E272
        assert "nbSelections"   in project_one['metrics'], "We check nbModels metrics is available"  # noqa:E272

        # We chek mandatory metadatas (Nothing)

    def test_get_projects_check_project_one_already_load(self, project_one):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200, "As no hash provider we shall have 200 response code"
        load = json.loads(resp.text)
        print(load)
        assert "hash_content" in load,  "We check hash_content are in the payload"

        hash_content = load["hash_content"]
        payload = {'prev_hash_content': hash_content}
        resp = requests.get(url=url, headers={}, params=payload)
        assert resp.status_code == 304, "As same hash than previous call is provide, we shall have 304 response code"
