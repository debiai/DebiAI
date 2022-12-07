# Get the list of samples ID of the project
def get_list(project_id, data_provider, data):
    # Option 1 : get samples id list
    # Option 2 : get samples id list from selections (intersection or union)
    # Option 3 : get samples id list from model results (common or not)
    # Option 4 : mix of 2 and 3
    # Return option : from and to for streaming purpose
    id_list = []
    nb_from_selection = 0
    nb_from_models = 0
    if "selectionIds" in data and len(data["selectionIds"]) > 0:
        # Option 2 : get samples id list from selections (intersection or union)
        selection_intersection = data["selectionIntersection"]
        for selection_id in data["selectionIds"]:
            selection_sample_ids = data_provider.get_selection_id_list(
                project_id, selection_id)
            if len(id_list) == 0:
                id_list = selection_sample_ids
            else:
                if selection_intersection:
                    id_list = list(set(id_list) & set(selection_sample_ids))
                    if len(id_list) == 0:
                        break
                else:
                    id_list = list(set(id_list) | set(selection_sample_ids))
        nb_from_selection = len(id_list)
    else:
        # Option 1 : get samples id list
        if "from" in data and "to" in data:
            id_list = data_provider.get_id_list(
                project_id, data["from"], data["to"])
        else:
            id_list = data_provider.get_id_list(project_id)

        nb_from_selection = len(id_list)

    if "modelIds" in data and len(data["modelIds"]) > 0 and len(id_list) > 0:
        # Option 3 : get samples id list from model results (common or not)
        common_results = data["commonResults"]
        model_result_ids = []
        for model_id in data["modelIds"]:
            # First get the model results id list
            model_sample_ids = data_provider.get_model_results_id_list(
                project_id, model_id)

            # Then get the common or not common samples id list
            if len(model_result_ids) == 0:
                model_result_ids = model_sample_ids
            else:
                if common_results:
                    model_result_ids = list(
                        set(model_result_ids) & set(model_sample_ids))
                    if len(model_result_ids) == 0:
                        break
                else:
                    model_result_ids = list(
                        set(model_result_ids) | set(model_sample_ids))

        # Finally get the common ids between the selection and the model results
        id_list = list(set(id_list) & set(model_result_ids))
        nb_from_models = len(model_result_ids)

    return {
        "samples": id_list,
        "nbSamples": len(id_list),
        "nbFromSelection": nb_from_selection,
        "nbFromModels": nb_from_models,
    }
