#############################################################################
# Imports
#############################################################################
import dataProviders.DataProviderException as DataProviderException
import dataProviders.dataProviderManager as data_provider_manager
import utils.samples.get_id_list as get_id_list

#############################################################################
# SAMPLES Management
#############################################################################


# Get the list of samples ID of the project
def get_list(projectId, data):
    # Option 1 : get samples id list
    # Option 2 : get samples id list from selections (intersection or union)
    # Option 3 : get samples id list from model results (common or not)
    # Option 4 : mix of 2 and 3
    # Return option : from and to for streaming purpose

    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    try:
            
        # Call our utility function
        data_id_list = get_id_list.get_list(projectId, data_provider, data)

        return data_id_list, 200
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code



# Get the list of samples ID of the project selection
def get_selection_list(projectId, selectionId):
    dataProviderId = projectId.split("|")[0]
    projectId = projectId.split("|")[1]
    data_provider = data_provider_manager.get_single_data_provider(dataProviderId)
    try:
        return data_provider.get_selection_id_list(projectId, selectionId)
    except DataProviderException.DataProviderException as e:
        return e.message, e.status_code
