#############################################################################
# Imports
#############################################################################
from config.init_config import get_config
from dataProviders.webDataProvider.WebDataProvider import WebDataProvider
import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.DataProviderException as DataProviderException

#############################################################################
# PROJECTS Management
#############################################################################


def get_data_providers():
    data_provider_list = data_provider_manager.get_data_provider_list()
    providers_formatted = []
    for data_provider in data_provider_list:
        data = {}
        if data_provider.type != "Python module Data Provider":
            data["url"] = data_provider.url
            data["status"] = data_provider.is_alive()

        data["name"] = data_provider.name
        data["type"] = data_provider.type

        providers_formatted.append(data)

    return providers_formatted, 200


def get_data_provider_info(dataProviderId):

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        info = data_provider.get_info()

        return info, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def post_data_providers(data):
    # Check if we are allowed to add data providers from the config file
    config = get_config()
    creation_allowed = config["DATA_PROVIDERS"]["creation"]
    if not creation_allowed:
        return "Data provider creation is not allowed", 403

    # Check if data provider already exists
    if data_provider_manager.data_provider_exists(data["name"]):
        return "Data provider already exists", 400

    # Check if data provider name is valid
    if not data_provider_manager.is_valid_name(data["name"]):
        return "Invalid data provider name", 400

    try:
        # Add data provider
        if data["type"] == "Web":
            data_provider_manager.add(WebDataProvider(data["url"], data["name"]))
        else:
            return "Invalid data provider type", 400

        return "", 204
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code


def delete_data_providers(dataProviderId):
    # Check if we are allowed to add data providers from the config file
    config = get_config()
    deletion_allowed = config["DATA_PROVIDERS"]["deletion"]
    if not deletion_allowed:
        return "Data provider deletion is not allowed", 403

    # Delete data provider
    try:
        data_provider_manager.delete(dataProviderId)
        return "", 204
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
