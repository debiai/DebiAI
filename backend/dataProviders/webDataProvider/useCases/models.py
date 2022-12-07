from dataProviders.webDataProvider.http.api import get_model_result, get_models, get_model_result_id_list
from utils.utils import timeNow

def get_models_info(url, project_id):
    
    # Models
    models = get_models(url, project_id)
    debiai_models = []
    for model in models:
        debiai_models.append(
            {
                "name": model["name"] if "name" in model else model["id"],
                "id": model["id"],
                "nbResults": model["nbResults"] if "nbResults" in model else 0,
                "creationDate": timeNow(),
                "updateDate": timeNow(),
                "metadata": {},
            }
        )
    
    return debiai_models   

def get_model_result_id(url, project_id , model_id):
    # Todo : Add route to call Id results for a Model (DP)
    # Todo : Add Some formating if data has to change
    return get_model_result_id_list(url, project_id, model_id)
    

def get_model_results(url, project_id, model_id, sample_list):
    
    return get_model_result(url, project_id, model_id, sample_list)

