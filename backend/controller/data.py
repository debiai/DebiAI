#############################################################################
# Imports
#############################################################################
import dataProviders.dataProviderManager as data_provider_manager
import dataProviders.DataProviderException as DataProviderException

#############################################################################
# Data Management
#############################################################################


def get_data(projectId, data):
    # return a project data from a list of ids
    data_provider_id = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    sampleIds = data["sampleIds"]

    try:
        # Find the data provider
        data_provider = data_provider_manager.get_single_data_provider(data_provider_id)

        # Ask for the data
        samples = data_provider.get_samples(projectId, sampleIds)

        if samples is not None:
            return {
                "data": samples,
                "dataMap": True,
            }, 200

        return (
            "Can't find samples for project "
            + projectId
            + " on data provider : "
            + data_provider_id,
            404,
        )
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
