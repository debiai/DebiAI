import modules.dataProviders.dataProviderManager as data_provider_manager
from modules.dataProviders.DataProviderException import DataProviderException

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
