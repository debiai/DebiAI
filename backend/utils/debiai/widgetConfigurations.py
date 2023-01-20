import os
import json
import utils.utils as utils
import uuid

CONF_PATH = "data/widgetConfigurations.json"

# Configuration file structure
# {
#     "widgetTitle": [
#         {
#             "id": ""
#             "name": ""
#             "description": "",
#             "projectId": ""
#             "dataProviderId": ""
#             "creationDate": 0
#
#             "configuration": {},
#         },
#         ...
#      ]
# }


def setup_widget_configurations():
    # Create the folder if it does not exist
    if not os.path.exists("data"):
        os.mkdir("data")

    # Create the file if it does not exist
    if not os.path.exists(CONF_PATH):
        _save_configurations({})


def get_configurations(widget_title):
    # Return the configurations list of the widget
    all_configurations = get_all_configurations()
    
    if widget_title in all_configurations:
        return all_configurations[widget_title]
    else:
        return []

def get_all_configurations():
    # Return the configurations list of all widgets
    try:
        with open(CONF_PATH) as json_file:
            return json.load(json_file)

    except FileNotFoundError:
        setup_widget_configurations()
        return {}
    except json.decoder.JSONDecodeError as e:
        print("Error while reading the widget configurations file")
        print(e)
        print("The file will be reset")
        _save_configurations({})
        return {}


def add_configuration(widget_title, data):
    # project_id, data_provider_id, conf_description, conf_name, conf
    # Add a new widget configuration
    configurations = get_all_configurations()

    if widget_title not in configurations:
        configurations[widget_title] = []

    # Generate id
    id = str(uuid.uuid1())

    configuration_to_add = {
        "id": id,
        "name": data["name"],
        "description": data["description"],
        "projectId": data["projectId"],
        "dataProviderId": data["dataProviderId"],
        "creationDate": utils.timeNow(),
        "configuration": data["configuration"],
    }

    # Save configuration
    configurations[widget_title].append(configuration_to_add)
    _save_configurations(configurations)


def delete_configuration(widget_title, id):
    # Delete the widget configuration by its name
    configurations = get_all_configurations()

    if widget_title in configurations:
        for configuration in configurations[widget_title]:
            if configuration["id"] == id:
                configurations[widget_title].remove(configuration)

        _save_configurations(configurations)
    

def _save_configurations(conf):
    # Update the json file
    try:
        with open(CONF_PATH, "w") as json_file:
            json.dump(conf, json_file)
    except FileNotFoundError:
        setup_widget_configurations()
        _save_configurations(conf)
