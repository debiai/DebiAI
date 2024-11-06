import os
import json
import debiaiServer.utils.utils as utils
import uuid
from debiaiServer.debiai_gui_utils import data_folder_path


LAYOUTS_PATH = data_folder_path + "/layouts.json"


# Layouts file structure
# [
#   {
#       "id": ""
#       "name": ""
#       "description": "",
#       "projectId": ""
#       "dataProviderId": ""
#       "creationDate": 0
#       "layout": [
#          # Widget position
#          {
#            "widgetKey": "parallelCoordinate",
#            "x": 0,
#            "y": 0,
#            "width": 0,
#            "height": 0,
#            "config": {}, # Widget config (optional)
#            "name": "", # Name given to the widget (optional)
#            "localFilters" : [{}],
#          },
#       ],
#       "selectedColorColumn": "col", # (optional)
#   },
#   ...
# ]


def setup_layouts():
    # Create the file if it does not exist
    if not os.path.exists(LAYOUTS_PATH):
        with open(LAYOUTS_PATH, "w") as json_file:
            json.dump([], json_file)
            json_file.flush()
            json_file.close()


def get_layouts():
    # Return the layouts list
    try:
        if os.path.getsize(LAYOUTS_PATH) == 0:
            # File exists but is empty, reset to default layouts
            print("Layouts file is empty, resetting to default layouts.")
            _save_layouts([])
            return []
        with open(LAYOUTS_PATH) as json_file:
            layouts = json.load(json_file)
            return layouts

    except FileNotFoundError:
        # File does not exist, create it with default layouts
        print("Layouts file not found, creating with default layouts.")
        setup_layouts()
        return []

    except json.decoder.JSONDecodeError as e:
        # Print the error and reset the file with default layouts
        print("Error while reading the layouts file:", e)
        print("The file will be reset to default layouts.")
        _save_layouts([])
        return []


def add_layout(data):
    # project_id, data_provider_id, conf_description, conf_name, conf
    # Add a new widget layout
    # Generate id
    id = str(uuid.uuid1())

    layout_to_add = []

    for widget in data["layout"]:
        widget_position = {
            "x": widget["x"],
            "y": widget["y"],
            "width": widget["width"],
            "height": widget["height"],
            "widgetKey": widget["widgetKey"],
        }

        keys = ["config", "name", "localFilters"]

        for key in keys:
            if key in widget:
                widget_position[key] = widget[key]

        layout_to_add.append(widget_position)

    file_to_add = {
        "id": id,
        "name": data["name"],
        "description": data["description"],
        "projectId": data["projectId"],
        "dataProviderId": data["dataProviderId"],
        "creationDate": utils.timeNow(),
        "layout": layout_to_add,
        "lastLayoutSaved": False,
    }

    if "selectedColorColumn" in data:
        file_to_add["selectedColorColumn"] = data["selectedColorColumn"]

    layouts = get_layouts()

    # Check if their is already a "last saved" layout
    if "lastLayoutSaved" in data and data["lastLayoutSaved"]:
        file_to_add["lastLayoutSaved"] = True

        for layout in layouts:
            if (
                layout["projectId"] == data["projectId"]
                and layout["dataProviderId"] == data["dataProviderId"]
                and "lastLayoutSaved" in layout
                and layout["lastLayoutSaved"]
            ):
                # Remove the "last saved" layout
                layouts.remove(layout)

    # Save layout
    layouts.append(file_to_add)
    _save_layouts(layouts)


def delete_layout(id):
    # Delete the widget layout by its name
    layouts = get_layouts()

    for layout in layouts:
        if layout["id"] == id:
            layouts.remove(layout)

    _save_layouts(layouts)


def _save_layouts(layouts, _second_try=False):
    # Update the json file
    try:
        with open(LAYOUTS_PATH, "w") as json_file:
            json.dump(layouts, json_file, ensure_ascii=False, indent=4)
            # Ensure data is written before closing the file
            json_file.flush()
            json_file.close()
    except FileNotFoundError:
        if not _second_try:
            setup_layouts()
            _save_layouts(layouts, _second_try=True)
        else:
            print("Error while saving the layouts file")
