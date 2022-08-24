import utils.debiaiUtils as debiaiUtils
import utils.config as configUtils
import time
from utils.export.methods.kafkaUtils import KafkaExportType

#############################################################################
#
# Export utils
#
# DebiAI allows to export data or selections to other services with
# different methods.
# This utils load and store the methods for all the projects
#
#############################################################################


export_types = [
    KafkaExportType()
]

export_methods = []


# Export types
def get_export_type(typeName):
    return [type for type in export_types if type.name == typeName][0]


def type_exist(typeName):
    return typeName in [type.name for type in export_types]


# Export methods
def get_export_methods():
    # Return all the export methods as a list of dictionaries
    return [method.to_dict() for method in export_methods]


def get_export_method(methodId):
    # Check the method id
    if not method_exist(methodId):
        raise Exception("Export method " + methodId + " not found")

    return [method for method in export_methods if method.id == methodId][0]


def method_exist(methodId):
    return methodId in [method.id for method in export_methods]


def load_export_methods():
    global export_methods

    print("========= Exports =========")

    # Load the export methods from the config file
    config = configUtils.get_config()

    if 'EXPORT_METHODS' in config:
        config_export_methods = config['EXPORT_METHODS']

        for method in config_export_methods:
            print("Configuring method " + method,
                  "[", config_export_methods[method], "]")

            parameters = config_export_methods[method].split(",")
            if len(parameters) == 0:
                raise "method " + method + " has no parameters, aborting"

            # Trim parameters
            for i in range(len(parameters)):
                parameters[i] = "".join(parameters[i].rstrip().lstrip())

            export_type_name = parameters[0]
            export_method = create_export_method(
                method, export_type_name, parameters[1:])

            export_methods.append(export_method)

    if len(export_methods) == 0:
        print("No export method configured")

    print("==========================")


def add_export_method(data):
    # Check the method type
    if not type_exist(data['type']):
        raise Exception("Method type " + data['type'] + " not found")

    # Check the method name
    if data['name'] in [method.name for method in export_methods]:
        raise Exception("An export method with the name '" +
                        data['name'] + "' already exists")

    export_method = create_export_method(
        data['name'], data['type'], data['parameters'])

    # The export method created from the dashboard are deletable
    export_method.deletable = True

    export_methods.append(export_method)

    return export_method.to_dict()


def create_export_method(name, type, parameters):
    # Check the method type
    if not type_exist(type):
        raise Exception("Export type '" + type + "' isn't supported, only " +
                        str([type.name for type in export_types]) + " are supported")

    # Get the export type
    export_type = get_export_type(type)

    # Create the method
    return export_type.export_method_class(name, parameters)


def delete_export_method(method_id):
    global export_methods
    # Check the method id
    if not method_exist(method_id):
        raise Exception("The expons method wasn't found")

    # Delete the method
    export_methods = [
        method for method in export_methods if method.id != method_id]
    return "method " + method_id + " deleted"


def exportSelection(projectId, data):
    method_id = data['exportMethodId']

    # Check the method id
    if not method_exist(method_id):
        raise Exception("method " + method_id + " not found")

    if not debiaiUtils.projectExist(projectId):
        raise Exception("project " + projectId + " not found")

    export_method = get_export_method(method_id)

    # Creation of the data selection to export
    project_name = debiaiUtils.getProjectNameFromId(projectId)

    project_sample_hashmap = debiaiUtils.getHashmap(projectId)
    sample_path = []
    for sample_hash in data['sampleHashList']:
        sample_path.append(project_sample_hashmap[sample_hash])

    id_list = []

    for id in sample_path:
        id_list.append({"id": id})

    data_to_export = {
        'origine': 'DebiAI',
        'project_name': project_name,
        'selection_name': data["selectionName"],
        'date': time.time(),
        'sample_ids': id_list
    }

    export_method.export(data_to_export)
    # Send the selection to Kafka
    # Export the data
    return "data exported"
