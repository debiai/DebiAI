import requests
import ujson as json
import pytest

appUrl = "http://localhost:3000/api/v1/"


class TestProjects:

    PYTHON_DATA_PROVIDER_ID: str = "Python module Data Provider"
    PYTHON_API_URL: str = "http://localhost:3000/api/v0/"
    PROJECT_NAME_1: str = "Test Default Project"

    def delete_project(self, project_name, fail_if_not_found: bool = False):

        url = (self.PYTHON_API_URL + "data-providers/" + self.PYTHON_DATA_PROVIDER_ID + "/projects/" + project_name)
        resp = requests.request("DELETE", url, headers={}, data={})
        if fail_if_not_found:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 200 or resp.status_code == 404

    def delete_projects(self):

        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        projects_response = json.loads(resp.text)
        project_list = projects_response

        for project in project_list:
            print(f"\nDeleting project {project['id']}")
            self.delete_project(project['id'])

    def create_project(self, project_name):
        url = self.PYTHON_API_URL + "projects"
        resp = requests.post(url=url, headers={}, json={"projectName": project_name})
        assert resp.status_code == 200

        # Get Id # WE DON NOT TEST THE API so we take as grand that good value are return for project ID
        data = json.loads(resp.text)
        test_project_id = data["id"]

        return test_project_id

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
        # delete if exists

        # create project one
        self.prj_one = self.create_project(self.PROJECT_NAME_1)

        yield
        print('\nProject init cleaning')

        # We reset project one if already exist
        self.delete_project(self.prj_one)
        # delete if exists

    @pytest.fixture
    def no_project(self):
        print('\nProjects reset  initiatization')
        self.delete_projects()
        yield
        print('\nProject reset cleaning')

    def test_get_project_response_structure(self):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        assert type(load) is list

    def test_get_project_response_void(self, no_project):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        assert len(load) == 0

    def test_get_projects_check_project_one(self, project_one):

        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        assert len(load) == 1
