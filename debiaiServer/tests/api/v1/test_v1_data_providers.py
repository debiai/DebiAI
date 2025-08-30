import requests
import ujson as json

appUrl = "http://localhost:3000/api/v1/"
test_data_provider_name = "test_create_data_provider"


class TestDataProvidersRegisty:
    data_providers = []

    def get_dataproviders(self):
        url = appUrl + "data-providers"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200, "As no hash provider we shall have 200 response code"
        load = json.loads(resp.text)

        assert "hash_content" in load
        assert "dataproviders" in load
        data_providers = load["dataproviders"]

        assert type(data_providers) is list
        return data_providers

    def get_dataprovider(self, name):

        data_providers = self.get_dataproviders()
        for dp in data_providers:
            self.check_provider(dp)
            if dp["name"] == name:
                return dp

        return None

    def check_provider(self, dp):
        assert type(dp) is dict
        assert "name" in dp
        assert "type" in dp

    def test_get_dataproviders_response_structure(self):
        url = appUrl + "data-providers"
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 200, "As no hash provider we shall have 200 response code"
        load = json.loads(resp.text)

        assert "hash_content" in load
        assert "dataproviders" in load
        data_providers = load["dataproviders"]

        assert type(data_providers) is list

        # Check mandatory field of data_providers
        for dp in data_providers:
            self.check_provider(dp)

    def test_get_intenal_provider(self):

        internal = self.get_dataprovider("Python module Data Provider")
        assert internal["type"] == "internal", "It's an internal type, check impact to the v0 API"

    def test_all_data_providers(self):

        data_providers = self.get_dataproviders()
        for dp in data_providers:
            url = appUrl + "data-providers/" + dp["name"]
            resp = requests.get(url=url, headers={})
            assert resp.status_code == 200
            dp = json.loads(resp.text)
            self.check_provider(dp)

    def test_add_data_provider(self):
        url = appUrl + "data-providers"
        data = {"name": test_data_provider_name, "type": "I DONT EXIST"}
        resp = requests.post(url=url, headers={}, json=data)
        assert resp.status_code == 400

    def test_add_web_data_provider(self):
        # test no url
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
        dp_from_list = self.get_dataprovider(test_data_provider_name)
        assert dp_from_list is not None
        assert dp_from_list["name"] == test_data_provider_name

    def test_delete_data_provider(self):
        url = appUrl + "data-providers/" + test_data_provider_name
        resp = requests.delete(url=url, headers={})
        assert resp.status_code == 204

        dp_from_list = self.get_dataprovider(test_data_provider_name)
        assert dp_from_list is None

        # Test that it no longer exists
        url = appUrl + "data-providers/" + test_data_provider_name
        resp = requests.get(url=url, headers={})
        assert resp.status_code == 404
