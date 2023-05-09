import requests
import ujson as json

appUrl = "http://localhost:3000/"
test_algo_provider_name = "test_create_algo_provider"

algo_provider_list = []


def test_get_algorithms():
    global algo_provider_list
    url = appUrl + "app/algo-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    print(resp.text)
    algo_providers = json.loads(resp.text)
    assert type(algo_providers) is list

    for algo_provider in algo_providers:
        assert type(algo_provider) is dict
        assert "name" in algo_provider
        assert "url" in algo_provider
        assert "status" in algo_provider
        assert "algorithms" in algo_provider

        assert type(algo_provider["name"]) is str
        assert type(algo_provider["url"]) is str
        assert type(algo_provider["status"]) is bool
        assert type(algo_provider["algorithms"]) is list

        for algo in algo_provider["algorithms"]:
            assert type(algo) is dict
            assert "id" in algo
            assert "inputs" in algo
            assert "outputs" in algo

            assert type(algo["id"]) is str
            assert type(algo["inputs"]) is list
            assert type(algo["outputs"]) is list

            for input in algo["inputs"]:
                assert type(input) is dict
                assert "name" in input
                assert "type" in input

                assert type(input["name"]) is str
                assert type(input["type"]) is str

            for output in algo["outputs"]:
                assert type(output) is dict
                assert "name" in output
                assert "type" in output

                assert type(output["name"]) is str
                assert type(output["type"]) is str

    algo_provider_list = algo_providers


def test_add_algo_provider():
    url = appUrl + "app/algo-providers"
    data = {"name": test_algo_provider_name, "url": "http://localhost:4000"}
    resp = requests.post(url=url, headers={}, json=data)
    assert resp.status_code == 204

    # Test that it exists
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    print(resp.text)
    algo_providers = json.loads(resp.text)
    assert type(algo_providers) is list
    assert len(algo_providers) == len(algo_provider_list) + 1
    assert any(
        algo_provider["name"] == test_algo_provider_name
        for algo_provider in algo_providers
    )


def test_delete_algo_provider():
    url = appUrl + "app/algo-providers/" + test_algo_provider_name
    resp = requests.delete(url=url, headers={})
    assert resp.status_code == 204

    # Test that it was removed from the list
    url = appUrl + "app/algo-providers"
    resp = requests.get(url=url, headers={})
    assert resp.status_code == 200
    print(resp.text)
    algo_providers = json.loads(resp.text)
    assert type(algo_providers) is list
    assert len(algo_providers) == len(algo_provider_list)
    assert not any(
        algo_provider["name"] == test_algo_provider_name
        for algo_provider in algo_providers
    )
