import uuid

#############################################################################
#
# Export type and method classes
#
# Those class are used to export data from a specific export type
#
#############################################################################


class ExportType:
    name = None
    parameters_definition = []
    export_method_class = None

    def to_dict(self):
        return {"name": self.name, "parameters": self.parameters_definition}


class ExportMethod:
    id = None
    type = None  # ExportType object
    name = None
    parameters = []

    deletable = False

    def __init__(self, type, name, parameters):
        self.id = uuid.uuid4().hex
        self.type = type
        self.name = name
        self.parameters = parameters

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.name,
            "name": self.name,
            "parameters": self.parameters,
            "parameterNames": self.type.parameters_definition,
            "deletable": self.deletable,
        }
