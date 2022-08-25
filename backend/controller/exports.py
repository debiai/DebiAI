import utils.export.exportUtils as exportUtils

#############################################################################
# Export API Management
#############################################################################

# exports.get_export_methods
# exports.post_export_method
# exports.delete_export_method
# exports.export


def get_export_methods():
    # ParametersCheck
    return exportUtils.get_export_methods(), 200


def post_export_method(data):
    try:
        return exportUtils.add_export_method(data), 200
    except Exception as e:
        return str(e), 400


def delete_export_method(exportMethodId):
    try:
        return exportUtils.delete_export_method(exportMethodId), 200
    except Exception as e:
        return str(e), 400


def exportSelection(projectId, data):
    try:
        return exportUtils.exportSelection(projectId, data), 200
    except Exception as e:
        return str(e), 400
