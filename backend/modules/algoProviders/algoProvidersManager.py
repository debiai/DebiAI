from config.init_config import get_config
from modules.algoProviders.AlgoProviderException import AlgoProviderException
from modules.algoProviders.AlgoProvider import AlgoProvider

algo_providers = []


def setup_algo_providers():
    print("==================== ALGO PROVIDERS ======================")
    config = get_config()
    algo_providers = config["ALGO_PROVIDERS"]

    keys = list(algo_providers.keys())
    values = list(algo_providers.values())

    # Add AlgoProviderss from config file
    print(" - Loading Algo providers  from config file")
    for i in range(len(algo_providers)):
        name = keys[i]
        url = values[i]

        # Remove trailing slash
        if url[-1] == "/":
            url = url[:-1]

        print(" - Adding AlgoProviders " + name + " from " + url + " - ")
        try:
            algo_provider = AlgoProvider(url, name)
            if algo_provider.is_alive():
                print(
                    "   AlgoProvider " + name + " added to list and already accessible"
                )
            else:
                print("   [ERROR] : AlgoProvider " + name + " Is not accessible now")

            add(algo_provider)

        except AlgoProviderException as e:
            print("   [ERROR] : AlgoProvider " + e.message + " Is not accessible now")

    if len(algo_providers) == 0:
        print("   No AlgoProviders found")


def add(algo_provider):
    algo_providers.append(algo_provider)


def get_algo_providers():
    return algo_providers

def get_algo_providers_json():
    algo_providers_json = []
    for algo_provider in algo_providers:
        algo_providers_json.append(algo_provider.to_json())
    return algo_providers_json

def algo_provider_exists(name):
    for d in algo_providers:
        if d.name == name:
            return True
    return False


def get_single_algo_provider(name):
    # Return the algo provider with the given name
    for d in algo_providers:
        if d.name == name:
            return d

    raise AlgoProviderException("Algo provider not found", 404)


def delete(name):
    for d in algo_providers:
        if d.name == name:
            algo_providers.remove(d)
            return
