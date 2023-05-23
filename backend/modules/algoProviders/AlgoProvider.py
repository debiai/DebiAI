# Class for AlgoProvider
import requests, json
from modules.algoProviders.AlgoProviderException import AlgoProviderException
from modules.algoProviders.integratedAlgoProvider.integratedAlgoProvider import (
    get_algorithms,
    use_algorithm,
)


class AlgoProvider:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.alive = False

    def is_alive(self):
        # Try to load algorithms
        self.alive = True if self.get_algorithms() is not None else False
        return self.alive

    def get_algorithms(self):
        try:
            r = requests.get(self.url + "/algorithms")
            return get_http_response(r)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ):
            return None

        except Exception as e:
            print("Error in get_algorithms")
            print(e)
            return None

    def to_json(self):
        algorithms = None
        if self.is_alive():
            algorithms = self.get_algorithms()

        return {
            "name": self.name,
            "url": self.url,
            "status": self.alive,
            "algorithms": algorithms,
        }

    def use_algorithm(self, algorithm_id, data):
        try:
            print("Using algoProvider: " + self.url)
            print("Using algorithm: " + algorithm_id)
            r = requests.post(
                self.url + "/algorithms/" + algorithm_id + "/run", json=data
            )
            if r.raise_for_status() is None:
                return get_valid_response(r)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as e:
            print("The algoProvider is not reachable")
            print(e)
            raise AlgoProviderException("AlgoProvider not reachable", 500)
        except requests.exceptions.HTTPError as e:
            print("The algoProvider returned an error")
            print(e)
            print(e.response.text)
            print(e.response.json())

            if "detail" in e.response.json():
                raise AlgoProviderException(e.response.json()["detail"], 400)

            if e.response.status_code == 500:
                raise AlgoProviderException(
                    "AlgoProvider internal server error: " + str(e), 500
                )
            elif e.response.status_code == 400:
                raise AlgoProviderException(e.response.text, 400)

            elif e.response.status_code == 404:
                raise AlgoProviderException(
                    "The algoProvider may not have this algorithm, " + e.response.text,
                    404,
                )
            else:
                raise AlgoProviderException(str(e), 400)


class IntegratedAlgoProvider(AlgoProvider):
    ### Integrated AlgoProvider
    # Used to expose the algorithms that are integrated
    # directly in DebiAI
    def __init__(self):
        self.url = "/app/algo-provider"
        self.name = "Integrated Algo-provider"
        self.alive = True

    def is_alive(self):
        return True

    def get_algorithms(self):
        return get_algorithms()

    def use_algorithm(self, algorithm_id, data):
        try:
            print("Using integrated algo-provider")
            print("Using algorithm: " + algorithm_id)
            return use_algorithm(algorithm_id, data)
        except TypeError as e:
            print("The integrated algo-provider returned an error")
            print(e)
            raise AlgoProviderException(algorithm_id + " returned an error: " + str(e), 400)
        except Exception as e:
            print("The integrated algo-provider returned an error")
            print(e)
            raise AlgoProviderException("AlgoProvider internal server error", 500)

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
