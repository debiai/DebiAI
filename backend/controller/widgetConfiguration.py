#############################################################################
# Imports
#############################################################################
#import utils.debiaiUtils as debiaiUtils
#import utils.debiai.widgetConfiguration as widgetConfUtils
import utils.utils as utils

#############################################################################
# Widget configuration Management
#############################################################################


def get_configurations(projectId):
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # Get configurations
    configurations = widgetConfUtils.getConfigurations(projectId)

    return configurations, 200


def post_configuration(projectId, data):
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # Save the selection
    widgetConfUtils.createConfiguration(
        projectId,
        data["widgetTitle"],
        data["name"],
        {
            "conf": data["configuration"],
            "name": data["name"],
            "description": data["description"],
            "creationDate": utils.timeNow(),
        },
    )

    return 200


def delete_configuration(projectId, data):
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    configurations = widgetConfUtils.getConfigurations(projectId)
    if data["widgetTitle"] in configurations:
        widgetConfUtils.deleteConfiguration(
            projectId, data["widgetTitle"], data["name"]
        )

    return widgetConfUtils.getConfigurations(projectId), 200
