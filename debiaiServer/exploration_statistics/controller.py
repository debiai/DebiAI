from .utils import get_columns_statistics


def get_columns_statistics_api(dataProviderId, projectId):
    return get_columns_statistics(dataProviderId, projectId), 200
