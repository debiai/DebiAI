import modules.dataProviders.webDataProvider.http.api as api
from modules.dataProviders.DataProviderException import DataProviderException


def get_models_info(url, project_id):
    # Models
    try:
        models = api.get_models(url, project_id)
        debiai_models = []
        for model_in in models:
            # TODO: Deal with error if no model or no id
            model = {
                "id": model_in["id"],
                # "creationDate": TODO,
                # "updateDate": TODO
                # "metadata": { TODO },
            }

            # Adding name and nbResults
            model["name"] = model_in["name"] if "name" in model_in else model_in["id"]
            if "nbResults" in model_in:
                model["nbResults"] = model_in["nbResults"]

            debiai_models.append(model)

        return debiai_models
    except DataProviderException:
        # The route may not be implemented in the data provider
        return []


def get_model_result_id(url, cache, project_id, model_id):
    # Todo : Add route to call Id results for a Model (DP)
    # Todo : Add Some formatting if data has to change

    id_list = cache.get_model_result_id_list(project_id, model_id)

    if id_list is None:
        id_list = api.get_model_result_id_list(url, project_id, model_id)
        cache.set_model_result_id_list(project_id, model_id, id_list)

    return id_list


def get_model_results(url, project_id, model_id, sample_list):
    return api.get_model_result(url, project_id, model_id, sample_list)


def delete_model(url, project_id, model_id):
    return api.delete_model(url, project_id, model_id)
