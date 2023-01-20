#############################################################################
# Imports
#############################################################################
import utils.debiai.widgetConfigurations as widgetConfUtils

#############################################################################
# Widget configuration Management
#############################################################################


def get_configurations(widgetTitle):
    configurations = widgetConfUtils.get_configurations(widgetTitle)
    return configurations, 200


def post_configuration(widgetTitle, data):
    widgetConfUtils.add_configuration(widgetTitle, data)
    return None, 204


def delete_configuration(widgetTitle, id):
    widgetConfUtils.delete_configuration(widgetTitle, id)
    return None, 204
