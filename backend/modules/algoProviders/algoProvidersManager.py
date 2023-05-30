from config.init_config import get_config
from modules.algoProviders.AlgoProviderException import AlgoProviderException
from modules.algoProviders.AlgoProvider import AlgoProvider, IntegratedAlgoProvider

algo_providers = []


def setup_algo_providers():
    print("==================== ALGO PROVIDERS ======================")
    config = get_config()
    config_algo_providers = config["ALGO_PROVIDERS"]

    keys = list(config_algo_providers.keys())
    values = list(config_algo_providers.values())

    # Add AlgoProviderss from config file
    print(" - Loading Algo providers from config file")
    for i in range(len(config_algo_providers)):
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

            algo_providers.append(algo_provider)

        except AlgoProviderException as e:
            print("   [ERROR] : AlgoProvider " + e.message + " Is not accessible now")

    # Add the integrated algo provider
    enable_integrated = config["ALGO_PROVIDERS_CONFIG"]["enable_integrated"]
    if enable_integrated:
        print(" - Adding integrated AlgoProviders")
        algo_provider = IntegratedAlgoProvider()
        nb_algos = len(algo_provider.get_algorithms())
        algo_providers.append(algo_provider)
        print("   Integrated AlgoProvider ready with " + str(nb_algos) + " algorithms")

    if len(algo_providers) == 0:
        print("   No AlgoProviders found")


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


def add(algo_provider):
    algo_providers.append(algo_provider)
    return


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
