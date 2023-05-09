# Class for AlgoProvider
import requests, json
from modules.algoProviders.AlgoProviderException import AlgoProviderException


class AlgoProvider:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.alive = None

    def is_alive(self):
        # Try to load algorithms
        self.alive = True if self.get_algorithms() is not None else False
        return self.alive

    def get_algorithms(self):
        try:
            r = requests.get(self.url + "/algorithms")
            return get_http_response(r)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return None

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "status": self.alive,
            "algorithms": self.get_algorithms(),
        }

# ==== Utils ====
def get_http_response(response):
    try:
        if response.raise_for_status() is None:
            return get_valid_response(response)
    except requests.exceptions.HTTPError:
        return get_error_response(response)


def get_valid_response(response):
    if response.status_code == 204:
        return True
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        return


def get_error_response(response):
    if response.status_code == 500:
        raise AlgoProviderException("AlgoProvider unexpected Error", 500)

    raise AlgoProviderException(response.text, response.status_code)
