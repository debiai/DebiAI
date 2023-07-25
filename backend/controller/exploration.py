import modules.dataProviders.dataProviderManager as data_provider_manager
from modules.dataProviders.DataProviderException import DataProviderException
from utils.samples.get_id_list import get_id_list_from_filters

#############################################################################
# Exploration Controller
#############################################################################


def get_columns_metrics(dataProviderId, projectId, data):
    try:
        # Get data provider
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        column_metrics = data_provider.get_columns_metrics(
            projectId, data["columnLabels"]
        )
        return column_metrics, 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_combinatorial_metrics(dataProviderId, projectId, data):
    try:
        # Get data provider
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        combinatorial_metrics = data_provider.get_combinatorial_metrics(
            projectId, data["columns"]
        )
        return combinatorial_metrics, 200
    except DataProviderException as e:
        return e.message, e.status_code


def get_data_id_list(dataProviderId, projectId, data):
    try:
        print("get_data_id_list")
        print(data)
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
        id_list = get_id_list_from_filters(data_provider, projectId, data)
        return id_list, 200
    except DataProviderException as e:
        return e.message, e.status_code
