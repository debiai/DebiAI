import requests
import ujson as json

appUrl = "http://localhost:3000/"
testWidgetKey = "testWidgetKey"
testConfigurationId = None


def delete_configuration(id):
    url = appUrl + "app/widgets/" + testWidgetKey + "/configurations/" + id
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 204


def test_get_configurations():
    url = appUrl + "app/widgets/" + testWidgetKey + "/configurations"
    resp = requests.request("GET", url, headers={}, data={})
    configurations = json.loads(resp.text)
    print(configurations)
    assert resp.status_code == 200
    assert type(configurations) is list

    # Remove all configurations
    for conf in configurations:
        assert type(conf) is dict
        assert "id" in conf
        delete_configuration(conf["id"])


def test_add_configuration():
    global testConfigurationId
    url = appUrl + "app/widgets/" + testWidgetKey + "/configurations"
    data = {
        "name": "testName",
        "description": "testDescription",
        "projectId": "testProjectId",
        "dataProviderId": "testDataProviderId",
        "configuration": {"testKey": "testValue"},
    }
    resp = requests.request("POST", url, headers={}, json=data)
    assert resp.status_code == 204

    # Check if the configuration was added
    resp = requests.request("GET", url, headers={}, data={})
    configurations = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(configurations) is list
    assert len(configurations) == 1
    assert configurations[0]["name"] == data["name"]
    assert configurations[0]["description"] == data["description"]
    assert configurations[0]["projectId"] == data["projectId"]
    assert configurations[0]["dataProviderId"] == data["dataProviderId"]
    assert type(configurations[0]["configuration"]) is dict
    assert (
        configurations[0]["configuration"]["testKey"]
        == data["configuration"]["testKey"]
    )

    assert "id" in configurations[0]
    assert type(configurations[0]["id"]) is str
    assert len(configurations[0]["id"]) > 0
    testConfigurationId = configurations[0]["id"]


def test_get_configurations_overview():
    url = appUrl + "app/widget-configurations"
    resp = requests.request("GET", url, headers={}, data={})
    configurations = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(configurations) is dict
    assert testWidgetKey in configurations
    assert configurations[testWidgetKey] == 1


def test_delete_configuration():
    # Remove the configuration
    delete_configuration(testConfigurationId)

    # Check if the configuration was removed
    url = appUrl + "app/widgets/" + testWidgetKey + "/configurations"
    resp = requests.request("GET", url, headers={}, data={})
    configurations = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(configurations) is list
    assert len(configurations) == 0
