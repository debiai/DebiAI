import uuid
import utils.debiaiUtils as debiaiUtils
import utils.config as configUtils

#############################################################################
#
# Export ulits
#
# DebiAI allows to export data or selections to other services with
# different methods.
# This utils load and store the methods for all the projects
#
#############################################################################


class ExportType:
    name = None
    parameters = {}

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def to_dict(self):
        return {
            'name': self.name,
            'parameters': self.parameters
        }


class ExportMethod:
    id = None
    type = None
    name = None
    parameters = {}

    def __init__(self, type, name, parameters):
        self.id = uuid.uuid4().hex
        self.type = type
        self.name = name
        self.parameters = parameters

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'parameters': self.parameters
        }


export_types = [
    ExportType("kafka", {"server": "string", "topic": "string"})
]
export_methods = []


def load_export_methods():
    global export_methods

    print("========= Exports =========")

    # Load the export methods from the config file
    config = configUtils.get_config()

    if 'exports' in config:
        config_export_methods = config['EXPORT_METHODS']

        for method in config_export_methods:
            print("Configuring method " + method,
                  "[", config_export_methods[method], "]")

            # if method['type'] not in [type.name for type in export_types]:
            #     raise "method type " + method['type'] + " not found"

    if len(export_methods) == 0:
        print("No export method configured")

    print("==========================")

    print("export_methods: " + str(export_methods))


def get_export_methods():
    # Return all the export methods as a list of dictionaries
    return [method.to_dict() for method in export_methods]


def method_exist(methodId):
    return methodId in [method.id for method in export_methods]


def add_export_method(data):
    # Check the method type
    if data['type'] not in [method.name for method in export_types]:
        raise "method type " + data['type'] + " not found"

    # Check the method name
    if data['name'] in [method.name for method in export_methods]:
        raise "method name " + data['name'] + " already exists"

    # Add the method
    export_methods.append(ExportMethod(
        data['type'], data['name'], data['parameters']))
    return "method " + data['name'] + " added"


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
