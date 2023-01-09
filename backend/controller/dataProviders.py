#############################################################################
# Imports
#############################################################################
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


def post_data_providers(data):
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
    data_provider_manager.delete(dataProviderId)
    return "", 204
