#############################################################################
# Imports
#############################################################################
from debiaiServer.config.init_config import get_config
import debiaiServer.modules.dataProviders.dataProviderManager as data_provider_manager
from debiaiServer.modules.dataProviders.DataProviderException import (
    DataProviderException,
)


def delete_data_providers(dataProviderId):
    # Check if we are allowed to add data providers from the config file
    config = get_config()
    deletion_allowed = config["DATA_PROVIDERS_CONFIG"]["deletion"]
    if not deletion_allowed:
        return "Data provider deletion is not allowed", 403

    # TODO LOIC: ack for name switch :
    if dataProviderId == "internal":
        dataProviderId = 'Python module Data Provider'

    # Delete data provider
    try:
        data_provider_manager.delete(dataProviderId)
        return None, 204
    except DataProviderException as e:
        return e.message, e.status_code


def get_data_provider_info(dataProviderId):

    # TODO LOIC: ack for name switch :
    if dataProviderId == "internal":
        dataProviderId = 'Python module Data Provider'

    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        info = data_provider.get_info()

        return info, 200
    except DataProviderException as e:
        return e.message, e.status_code
