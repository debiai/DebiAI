#############################################################################
# Imports
#############################################################################
from config.init_config import get_config
from utils.utils import is_url_valid
import modules.algoHub.algoHubManager as algo_hub_manager
from modules.algoHub.algoHub import AlgoHub

#############################################################################
# Algo hub Management
#############################################################################


def get_algorithms():
    algorithms = algo_hub_manager.get_algorithms()
    return algorithms, 200


def post_algo_hub(data):
    # Check if we are allowed to add AlgoHubs from the config file
    config = get_config()
    creation_allowed = config["ALGO_HUB"]["creation"]
    if not creation_allowed:
        return "AlgoHub creation is not allowed", 403

    # Check if algoHub already exists
    if algo_hub_manager.algo_hub_exists(data["name"]):
        return "AlgoHub already exists", 400

    # Check if algoHub name is valid
    if not algo_hub_manager.is_valid_name(data["name"]):
        return "Invalid algoHub name", 400

    # Add algoHUub
    # Check if url is valid
    if "url" not in data:
        return "A url must be provided", 400

    if not is_url_valid(data["url"]):
        return "Invalid url", 400

    algo_hub_manager.add(AlgoHub(data["url"], data["name"]))

    return None, 204


def delete_algo_hub(algoHubId):
    # Check if we are allowed to add AlgoHubs from the config file
    config = get_config()
    deletion_allowed = config["ALGO_HUB"]["deletion"]
    if not deletion_allowed:
        return "AlgoHub deletion is not allowed", 403

    # Delete algub
    try:
        algo_hub_manager.delete(algoHubId)
        return None, 204
    except algoHubException.algoHubException as e:
        return e.message, e.status_code
