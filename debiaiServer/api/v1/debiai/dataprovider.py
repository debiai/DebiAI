#############################################################################
# Imports
#############################################################################
from debiaiServer.config.init_config import get_config
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)
from debiaiServer.api.v1.debiai.utils import make_hash


def format_data_provider_info(data_provider):
    data = {
        "id": data_provider.id,
        "status": True,
        "name": data_provider.name,
        "type": data_provider.type,
        "tags": [],
        "metadata": {},
        "metrics": {},
    }
    print("NAME ", data_provider.name)

    provider_info = data_provider.get_info()
    if "canDelete" in provider_info and provider_info["canDelete"]["models"]:
        data["tags"].append("canDeleteModels")
    if "canDelete" in provider_info and provider_info["canDelete"]["projects"]:
        data["tags"].append("canDeleteProject")
    if "canDelete" in provider_info and provider_info["canDelete"]["selections"]:
        data["tags"].append("canDeleteSelections")
    if "version" in provider_info:
        data["metadata"]["version"] = provider_info["version"]

    if "maxResultByRequest" in provider_info:
        data["metrics"]["maxResultByRequest"] = provider_info["maxResultByRequest"]
    if "maxSampleDataByRequest" in provider_info:
        data["metrics"]["maxSampleDataByRequest"] = provider_info[
            "maxSampleDataByRequest"
        ]
    if "maxSampleIdByRequest" in provider_info:
        data["metrics"]["maxSampleIdByRequest"] = provider_info["maxSampleIdByRequest"]

    if data_provider.name != "Python module Data Provider":
        data["metadata"]["external_url"] = data_provider.url

    return data


def get_data_provider_info(dataProviderId):

    # As Parquet not yet supported we force json_block:
    if dataProviderId == "json_block":
        dataProviderId = "Python module Data Provider"

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        data = format_data_provider_info(data_provider)

        return data, 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_data_providers(prev_hash_content=None):
    data_provider_list = data_provider_manager.get_data_provider_list()
    providers_formatted = []

    for data_provider in data_provider_list:
        try:
            data = format_data_provider_info(data_provider)
        except DataProviderException as e:
            data = {
                "id": data_provider.id,
                "status": False,
                "name": data_provider.name,
                "type": data_provider.type,
                "tags": [],
                "metadata": {
                    "status_code": e.status_code,
                    "message": e.message,
                },
                "metrics": {},
            }

        providers_formatted.append(data)

    new_hash = "data_" + str(make_hash(providers_formatted))
    # We add a prefix to avoir empty string

    print(
        new_hash,
        " <=> ",
        prev_hash_content,
        type(new_hash),
        type(prev_hash_content),
        new_hash == prev_hash_content,
    )
    if new_hash == prev_hash_content:
        return None, 304
    else:
        providers_answer = {
            "dataproviders": providers_formatted,
            "hash_content": new_hash,
        }
        return providers_answer, 200


def delete_data_providers(dataProviderId):
    # Check if we are allowed to add data providers from the config file
    config = get_config()
    deletion_allowed = config["DATA_PROVIDERS_CONFIG"]["deletion"]
    if not deletion_allowed:
        return "Data provider deletion is not allowed", 403

    # To remove when legacy API V0 removal
    if dataProviderId == "json_block":
        dataProviderId = "Python module Data Provider"

    # Delete data provider
    try:
        data_provider_manager.delete(dataProviderId)
        return None, 204
    except DataProviderException as e:
        return e.message, e.status_code
