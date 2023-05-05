from config.init_config import get_config
from modules.algoHub.AlgoHubException import AlgoHubException
from modules.algoHub.AlgoHub import AlgoHub

algo_hub_list = []


def setup_algo_hub():
    print("==================== ALGO HUB ======================")
    config = get_config()
    algo_hub_config = config["ALGO_HUB_LIST"]

    keys = list(algo_hub_config.keys())
    values = list(algo_hub_config.values())

    # Add AlgoHubs from config file
    print(" - Loading Algo Hub from config file")
    for i in range(len(algo_hub_config)):
        name = keys[i]
        url = values[i]

        # Remove trailing slash
        if url[-1] == "/":
            url = url[:-1]

        print(" - Adding AlgoHub " + name + " from " + url + " - ")
        try:
            algo_hub = AlgoHub(url, name)
            if algo_hub.is_alive():
                print(
                    "   AlgoHub "
                    + name
                    + " added to AlgoHub list and already accessible"
                )
            else:
                print("   [ERROR] : AlgoHub " + name + " Is not accessible now")

            add(algo_hub)

        except AlgoHubException as e:
            print("   [ERROR] : AlgoHub " + e.message + " Is not accessible now")

    if len(algo_hub_list) == 0:
        print("   No AlgoHub found")


def algo_hub_exists(name):
    for d in algo_hub_list:
        if d.name == name:
            return True
    return False


def add(algo_hub):
    algo_hub_list.append(algo_hub)
    return


def get_algo_hub_list():
    return algo_hub_list


def get_single_algo_hub(name):
    # Check if the data provider is not disabled
    config = get_config()
    if not config["ALGO_HUB"]["enabled"]:
        raise AlgoHubException("Python module data provider is disabled", 403)

    # Return the data provider with the given name
    for d in algo_hub_list:
        if d.name == name:
            return d

    raise AlgoHubException("Data provider not found", 404)


def delete(name):
    for d in algo_hub_list:
        if d.name == name:
            if d.type == "Python module Data Provider":
                raise AlgoHubException(
                    "Python module data provider cannot be deleted", 403
                )

            algo_hub_list.remove(d)
            return
