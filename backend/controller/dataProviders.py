#############################################################################
# Imports
#############################################################################
from dataProviders.webDataProvider.WebDataProvider import WebDataProvider
from dataProviders.pythonDataProvider.PythonDataProvider import PythonDataProvider
import dataProviders.dataProviderManager as data_provider_manager

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
    if data["type"] == "Web":
        data_provider_manager.add(WebDataProvider(data["url"], data["name"]))
    else:
        data_provider_manager.add(PythonDataProvider())

    return "", 204


def delete_data_providers(dataProviderId):
    data_provider_manager.delete(dataProviderId)
    return "", 204
