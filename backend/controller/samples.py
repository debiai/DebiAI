#############################################################################
# Imports
#############################################################################
import modules.dataProviders.DataProviderException as DataProviderException
import modules.dataProviders.dataProviderManager as data_provider_manager
import utils.samples.get_id_list as get_id_list

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
def get_list(dataProviderId, projectId, data):
    # Option 1 : get samples id list
    # Option 2 : get samples id list from selections (intersection or union)
    # Option 3 : get samples id list from model results (common or not)
    # Option 4 : mix of 2 and 3
    # Return option : from and to for streaming purpose
    try:
        data_provider = data_provider_manager.get_single_data_provider(dataProviderId)

        # Call our utility function
        data_id_list = get_id_list.get_list(data_provider, projectId, data)

        return data_id_list, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
