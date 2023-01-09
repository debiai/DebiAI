from config.init_config import get_config
from dataProviders.webDataProvider.WebDataProvider import WebDataProvider
from dataProviders.pythonDataProvider.PythonDataProvider import PythonDataProvider
import dataProviders.DataProviderException as DataProviderException

data_providers_list = []


def setup_data_providers():
    print("================== DATA PROVIDERS ==================")
    config = get_config()
    web_data_provider_config = config["WEB_DATA_PROVIDERS"]
    python_module_data_provider_config = config["PYTHON_MODULE_DATA_PROVIDER"]

    keys = list(web_data_provider_config.keys())
    values = list(web_data_provider_config.values())

    # Web Data Providers
    for i in range(len(web_data_provider_config)):
        name = keys[i]
        url = values[i]
        print(" - Adding external data Provider " + name + " from " + url + " - ")
        try:
            data_provider = WebDataProvider(url, name)
            if data_provider.is_alive():
                print(
                    "   Data Provider "
                    + name
                    + " added to Data Providers list and already accessible"
                )
            else:
                print("   [ERROR] : Data Provider " + name + " Is not accessible now")
            add(data_provider)
        except DataProviderException.DataProviderException as e:
            print("   [ERROR] : Data Provider " + e.message + " Is not accessible now")

    # Python Data Providers
    if python_module_data_provider_config["enabled"] != False:
        print(" - Adding Python Module data Provider")
        add(PythonDataProvider())

    if len(data_providers_list) == 0:
        print("Warning, No data providers setup")


def data_provider_exists(name):
    for d in data_providers_list:
        if d.name == name:
            return True
    return False


def is_valid_name(name):
    # /, &, | are not allowed in data provider names
    if (
        "/" in name
        or "&" in name
        or "|" in name
        or len(name) == 0
        or len(name) > 50
        or name[0] == " "
        or name[-1] == " "
    ):
        return False

    return True


def add(data_provider):
    data_providers_list.append(data_provider)
    return


def get_data_provider_list():
    return data_providers_list


def get_single_data_provider(name):
    for d in data_providers_list:
        if d.name == name:
            return d

    raise DataProviderException.DataProviderException("Data provider not found", 404)


def delete(name):
    for d in data_providers_list:
        if d.name == name:
            if d.type == "Python module Data Provider":
                raise DataProviderException.DataProviderException(
                    "Python module data provider cannot be deleted", 403
                )

            data_providers_list.remove(d)
            return
