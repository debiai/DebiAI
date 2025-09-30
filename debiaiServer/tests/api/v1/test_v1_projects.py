import requests
import ujson as json
import pytest

appUrl = "http://localhost:3000/api/v1/"


class TestProjects:

    PYTHON_DATA_PROVIDER_ID: str = "Python module Data Provider"
    PYTHON_API_URL: str = "http://localhost:3000/api/v0/"
    PROJECT_NAME_1: str = "Test Default Project"

    def delete_project(self, project_name, fail_if_not_found: bool = False):

        url = (
            self.PYTHON_API_URL
            + "data-providers/"
            + self.PYTHON_DATA_PROVIDER_ID
            + "/projects/"
            + project_name
        )
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
        assert "projects" in projects_response
        print(projects_response)
        project_list = projects_response["projects"]
        print(project_list)

        for project in project_list:
            print(project)
            print(f"\nDeleting project {project['id']}")
            self.delete_project(project["id"])

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
        print("\nProjects one initialization")

        # We reset project one if already exist
        self.delete_project(self.PROJECT_NAME_1)
        # delete if exists

        # create project one
        self.prj_one = self.create_project(self.PROJECT_NAME_1)

        yield
        print("\nProject init cleaning")

        # We reset project one if already exist
        self.delete_project(self.prj_one)
        # delete if exists

    @pytest.fixture
    def no_project(self):
        print("\nProjects reset  initialization")
        self.delete_projects()
        yield
        print("\nProject reset cleaning")

    def test_get_project_response_structure(self):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        assert "projects" in load
        project_list = load["projects"]
        assert type(project_list) is list
        assert "hash_content" in load

    def test_get_project_response_void(self, no_project):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200
        load = json.loads(resp.text)
        assert "projects" in load
        project_list = load["projects"]
        assert len(project_list) == 0

    def test_get_projects_check_project_one_empty(self, project_one):

        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert (
            resp.status_code == 200
        ), "As no hash provider we shall have 200 response code"
        load = json.loads(resp.text)
        print(load)
        assert "projects" in load, "We check projects are in the payload"

        project_list = load["projects"]
        assert len(project_list) == 1, "We check only one project exist"

        project_one = project_list[0]
        assert project_one["id"] == self.PROJECT_NAME_1, "We check The project name"

        # We check project expected properties
        assert (
            "name" in project_one
        ), "We check name  are in the projects payload"  # noqa:E272
        assert (
            "updateDate" in project_one
        ), "We check creationDate  are in the projects payload"  # noqa:E272
        assert (
            "creationDate" in project_one
        ), "We check creationDate  are in the projects payload"  # noqa:E272
        assert (
            "dataProviderId" in project_one
        ), "We check dataProviderId  are in the projects payload"  # noqa:E272
        assert (
            "tags" in project_one
        ), "We check tags  are in the projects payload"  # noqa:E272
        assert (
            "metadata" in project_one
        ), "We check metadata  are in the projects payload"  # noqa:E272
        assert (
            "metrics" in project_one
        ), "We check metrics  are in the projects payload"  # noqa:E272

        # We check mandatory metrics
        assert (
            "nbModels" in project_one["metrics"]
        ), "We check nbModels metrics is available"  # noqa:E272
        assert (
            "nbSamples" in project_one["metrics"]
        ), "We check nbModels metrics is available"  # noqa:E272
        assert (
            "nbSelections" in project_one["metrics"]
        ), "We check nbModels metrics is available"  # noqa:E272

        # We check mandatory metadata (Nothing)

    def test_get_projects_check_project_one_already_load(self, project_one):
        url = appUrl + "projects"
        resp = requests.get(url=url, headers={})
        assert (
            resp.status_code == 200
        ), "As no hash provider we shall have 200 response code"
        load = json.loads(resp.text)
        print(load)
        assert "hash_content" in load, "We check hash_content are in the payload"

        hash_content = load["hash_content"]
        payload = {"prev_hash_content": hash_content}
        resp = requests.get(url=url, headers={}, params=payload)
        assert (
            resp.status_code == 304
        ), "As same hash than previous call is provide, we shall have 304 response code"
