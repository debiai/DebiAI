#############################################################################
# Imports
#############################################################################
from config.init_config import get_config
from utils.utils import is_url_valid, is_valid_name
import modules.algoHub.algoHubManager as algo_hub_manager
from modules.algoHub.AlgoHubException import AlgoHubException
from modules.algoHub.AlgoHub import AlgoHub

#############################################################################
# Algo hub Management
#############################################################################


def get_algorithms():
    algorithms = algo_hub_manager.get_algorithms()
    return algorithms, 200


def post_algo_hub(data):
    # Check if we are allowed to add AlgoHubs from the config file
    config = get_config()
    creation_allowed = config["ALGO_HUB_CONFIG"]["creation"]
    if not creation_allowed:
        return "AlgoHub creation is not allowed", 403

    # Check if algoHub already exists
    if algo_hub_manager.algo_hub_exists(data["name"]):
        return "AlgoHub already exists", 400

    # Check if algoHub name is valid
    if not is_valid_name(data["name"]):
        return "Invalid algoHub name", 400

    # Add algoHUub
    # Check if url is valid
    if "url" not in data:
        return "A url must be provided", 400

    if not is_url_valid(data["url"]):
        return "Invalid url", 400

    algo_hub_manager.add(AlgoHub(data["url"], data["name"]))

    return None, 204


def use_algo(algoHubName, data):
    # Check if algoHub exists
    if not algo_hub_manager.algo_hub_exists(algoHubName):
        return "AlgoHub does not exists", 404

    # Use algoHub
    algo_hub_manager.use(algoHubName)

    return None, 204

def delete_algo_hub(algoHubName):
    # Check if we are allowed to add AlgoHubs from the config file
    config = get_config()
    deletion_allowed = config["ALGO_HUB_CONFIG"]["deletion"]
    if not deletion_allowed:
        return "AlgoHub deletion is not allowed", 403

    # Delete algub
    try:
        algo_hub_manager.delete(algoHubName)
        return None, 204
    except AlgoHubException as e:
        return e.message, e.status_code
