import requests
import ujson as json

appUrl = "http://localhost:3000/"
test_data_provider_name = "test_create_data_provider"

data_providers = []


def test_get_data_providers():
    global data_providers
    url = appUrl + "data-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    print(resp.text)
    assert type(json.loads(resp.text)) is list

    for dp in json.loads(resp.text):
        assert type(dp) is dict
        assert "name" in dp
        assert "type" in dp

    data_providers = json.loads(resp.text)


def test_get_data_provider():
    for dp in data_providers:
        url = appUrl + "data-providers/" + dp["name"]
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200


def test_add_data_provider():
    url = appUrl + "data-providers"
    data = {"name": test_data_provider_name, "type": "I DONT EXIST"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400


def test_add_web_data_provider():
    # Test no url
    url = appUrl + "data-providers"
    data = {"name": test_data_provider_name, "type": "Web"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400

    # Test bad url
    data = {"name": test_data_provider_name, "type": "Web", "url": ""}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400
    data = {"name": test_data_provider_name, "type": "Web", "url": "I DONT EXIST"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400

    # Test good url
    data = {
        "name": test_data_provider_name,
        "type": "Web",
        "url": "http://localhost:4000",
    }
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 204

    # Test that it exists
    url = appUrl + "data-providers/" + test_data_provider_name
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200

    # Test that it was added to the list
    url = appUrl + "data-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list
    assert len(json.loads(resp.text)) == len(data_providers) + 1
    assert any(dp["name"] == test_data_provider_name for dp in json.loads(resp.text))


def test_delete_data_provider():
    url = appUrl + "data-providers/" + test_data_provider_name
    resp = requests.delete(url=url, headers={})
    assert resp.status_code == 204

    # Test that it was removed from the list
    url = appUrl + "data-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list
    assert len(json.loads(resp.text)) == len(data_providers)
    assert not any(
        dp["name"] == test_data_provider_name for dp in json.loads(resp.text)
    )

    # Test that it no longer exists
    url = appUrl + "data-providers/" + test_data_provider_name
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 404
