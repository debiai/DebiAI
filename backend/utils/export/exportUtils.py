import utils.debiaiUtils as debiaiUtils
import utils.config as configUtils
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

            # Check the method type
            if not type_exist(export_type_name):
                raise "method type " + export_type_name + " isn't supported, only " + \
                    str([type.name for type in export_types]) + " are supported"

            # Get the export type
            export_type = get_export_type(export_type_name)

            # Create the method
            export_methods.append(
                export_type.export_method_class(method, parameters[1:]))

            print("Method " + method + " added")

    if len(export_methods) == 0:
        print("No export method configured")

    print("==========================")

    print("export_methods: " + str(export_methods))


def get_export_methods():
    # Return all the export methods as a list of dictionaries
    return [method.to_dict() for method in export_methods]


def get_export_type(typeName):
    return [type for type in export_types if type.name == typeName][0]


def method_exist(methodId):
    return methodId in [method.id for method in export_methods]


def type_exist(typeName):
    return typeName in [type.name for type in export_types]


def add_export_method(data):
    # # Check the method type
    # if not type_exist(data['type']):
    #     raise "method type " + data['type'] + " not found"

    # # Check the method name
    # if data['name'] in [method.name for method in export_methods]:
    #     raise "method name " + data['name'] + " already exists"

    # # Add the method
    # export_methods.append(ExportMethod(
    #     data['type'], data['name'], data['parameters']))
    # return "method " + data['name'] + " added"
    pass


def delete_export_method(methodId):
    # Check the method id
    if not method_exist(methodId):
        raise "method " + methodId + " not found"

    # Delete the method
    export_methods = [
        method for method in export_methods if method.id != methodId]
    return "method " + methodId + " deleted"


def export(projectId, methodId, data):
    # Check the method id
    if not method_exist(methodId):
        raise "method " + methodId + " not found"

    if not debiaiUtils.projectExist(projectId):
        raise "project " + projectId + " not found"

    # Export the data
    return "data exported"

    # project_name = debiaiUtils.getProjectNameFromId(projectId)

    # # Send the selection to Kafka
    # project_sample_hashmap = debiaiUtils.getHashmap(projectId)
    # sample_path = []
    # for sample_hash in selectionInfo['samples']:
    #     sample_path.append(project_sample_hashmap[sample_hash])

    # kafkaUtils.send_sample_selection(
    #     project_name,
    #     data['selectionName'],
    #     sample_path
    # )
    # project_name: str, selection_name: str, sample_ids: list):
    #         # Construct id list
    #         id_list = []

    #         for id in sample_ids:
    #             id_list.append({"id": id})

    #         producer.send(KAFKA_SELECTIONS_TOPIC, {
    #             'origine': 'debiai',
    #             'project_name': project_name,
    #             'selection_name': selection_name,
    #             'date': time.time(),
    #             'sample_ids': id_list
    #         })
