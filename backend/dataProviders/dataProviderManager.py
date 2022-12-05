from config.init_config import get_config
# from dataProviders.webDataProvider.WebDataProvider import WebDataProvider
from dataProviders.pythonDataProvider.PythonDataProvider import PythonDataProvider

data_providers_list = []


def setup_data_providers():
    print("================= SET UP DATA PROVIDERS ==================")
    config = get_config()
    data_provider_config = config["DATA_PROVIDERS"]
    
    keys = list(data_provider_config.keys())
    values = list(data_provider_config.values())

    # Web Data Providers
    for i in range(len(data_provider_config)):
        name = keys[i]
        url = values[i]
        add(WebDataProvider(url, name))
    
    # Python Data Providers
    # TODO: make it optional in the config file
    add(PythonDataProvider())

    return
    
def add(data_provider):
    data_providers_list.append(data_provider)
    return

def get_data_provider_list():
    return data_providers_list

def get_single_data_provider(name):
    for d in data_providers_list:
        if d.name == name:
            return d
    return

def delete(name):
    for d in data_providers_list:
        if d.name == name:
            data_providers_list.remove(d)
            return
    return

    
        