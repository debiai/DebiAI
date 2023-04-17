import dataProviders.webDataProvider.http.api as api
from dataProviders.DataProviderException import DataProviderException


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
    except DataProviderException as e:
        # The route may not be implemented in the data provider
        return []


def get_model_result_id(url, project_id, model_id):
    # Todo : Add route to call Id results for a Model (DP)
    # Todo : Add Some formating if data has to change
    rsp = api.get_model_result_id_list(url, project_id, model_id)
    return rsp


def get_model_results(url, project_id, model_id, sample_list):
    return api.get_model_result(url, project_id, model_id, sample_list)


def delete_model(url, project_id, model_id):
    return api.delete_model(url, project_id, model_id)
