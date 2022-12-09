from config.init_config import get_config
from dataProviders.webDataProvider.WebDataProvider import WebDataProvider
from dataProviders.pythonDataProvider.PythonDataProvider import PythonDataProvider

data_providers_list = []


def setup_data_providers():
    print("================= SET UP DATA PROVIDERS ==================")
    config = get_config()
    data_provider_config = config["DATA_PROVIDERS"]
    
    internal_data_provider = data_provider_config.pop("Internal_data_provider", False)
    
    keys = list(data_provider_config.keys())
    values = list(data_provider_config.values())

    # Web Data Providers
    for i in range(len(data_provider_config)):
        name = keys[i]
        url = values[i]
        print("======== Adding external data Provider " + name + " from " + url + "========")
        add(WebDataProvider(url, name))
    
    # Python Data Providers
    
    if bool(internal_data_provider) == True:
        print("======== Adding internal data Provider ========")
        add(PythonDataProvider())
        print(PythonDataProvider().name)

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

    
        