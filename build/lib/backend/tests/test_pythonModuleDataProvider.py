import requests
import ujson as json

PYTHON_DATA_PROVIDER_ID = "Python module Data Provider"
appUrl = "http://localhost:3000/"
test_project_name = "test_create_project"
test_project_id = None

# ============== PROJECTS =================


def test_get_projects():
    url = appUrl + "projects"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list


def test_get_bad_project():
    projectId = "I_DO_NOT_EXIST"
    url = (
        appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + projectId
    )
    resp = requests.request("GET", url, headers={}, data={})
    assert resp.status_code == 404

    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 404


def test_create_project_noName():
    # create
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={})
    assert resp.status_code == 400


def test_create_project():
    global test_project_id
    # delete if exists
    projectId = test_project_name
    url = (
        appUrl + "data-providers/" + PYTHON_DATA_PROVIDER_ID + "/projects/" + projectId
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200 or resp.status_code == 404

    # create
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={"projectName": test_project_name})
    assert resp.status_code == 200

    # Get Id
    data = json.loads(resp.text)
    test_project_id = data["id"]
    assert test_project_id is not None
    assert len(test_project_id) > 0
    assert type(test_project_id) is str

    # Test can't create same project
    resp = requests.post(url=url, headers={}, json={"projectName": test_project_name})
    assert resp.status_code == 400
    assert "already exists" in resp.text


def test_get_project():
    # Find back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    assert type(proj) is dict
    assert type(proj["columns"]) is list
    assert proj["models"] == []
    assert len(proj["name"]) > 0
    assert proj["name"] == test_project_name


def test_remove_project():
    # Project exists back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 200

    # remove
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200

    # Dont Find back
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 404

    # Cant remove again
    url = (
        appUrl
        + "data-providers/"
        + PYTHON_DATA_PROVIDER_ID
        + "/projects/"
        + test_project_id
    )
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 404


def test_project_nameTooLong():
    testProjectName = "a" * 256
    url = appUrl + "projects"
    payload = {"projectName": testProjectName, "blockLevelInfo": []}
    headers = {"content-type": "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 400
