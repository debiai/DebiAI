import requests
import ujson as json

appUrl = "http://localhost:3000/"
test_algo_hub = "test_create_algo_hub"

algo_hub_list = []


def test_get_algorithms():
    global algo_hub_list
    url = appUrl + "algo-hubs"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    print(resp.text)
    algo_list = json.loads(resp.text)
    assert type(algo_list) is list

    for algo_hub in algo_list:
        assert type(algo_hub) is dict
        assert "name" in algo_hub
        assert "url" in algo_hub

    algo_hub_list = algo_list


def test_add_algo_hub():
    url = appUrl + "data-providers"
    data = {"name": test_algo_hub, "type": "I DONT EXIST"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400


def test_add_web_algo_hub():
    # Test no url
    url = appUrl + "data-providers"
    data = {"name": test_algo_hub, "type": "Web"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400

    # Test bad url
    data = {"name": test_algo_hub, "type": "Web", "url": ""}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400
    data = {"name": test_algo_hub, "type": "Web", "url": "I DONT EXIST"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 400

    # Test good url
    data = {
        "name": test_algo_hub,
        "type": "Web",
        "url": "http://localhost:4000",
    }
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 204

    # Test that it exists
    url = appUrl + "data-providers/" + test_algo_hub
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200

    # Test that it was added to the list
    url = appUrl + "data-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list
    assert len(json.loads(resp.text)) == len(algo_hub_list) + 1
    assert any(algo_hub["name"] == test_algo_hub for algo_hub in json.loads(resp.text))


def test_delete_algo_hub():
    url = appUrl + "data-providers/" + test_algo_hub
    resp = requests.delete(url=url, headers={})
    assert resp.status_code == 204

    # Test that it was removed from the list
    url = appUrl + "data-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list
    assert len(json.loads(resp.text)) == len(algo_hub_list)
    assert not any(algo_hub["name"] == test_algo_hub for algo_hub in json.loads(resp.text))

    # Test that it no longer exists
    url = appUrl + "data-providers/" + test_algo_hub
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 404
