from dataProviders.webDataProvider.http.api import get_model_result, get_models

def get_models_info(url, project_id):
    
    return get_models(url, project_id)

def get_model_results(url, project_id, model_id, sample_list):
    
    return get_model_result(url, project_id, model_id, sample_list)
