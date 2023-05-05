import utils.dataProviders.dataProviderManager as dataProviderManager
import utils.exportMethods.exportUtils as exportUtils
import utils.widgetConfigurations.widgetConfigurations as widgetConfUtils
import utils.layouts.layouts as layoutsUtils
import config.init_config as config


def init():
    # Init config file
    config.init_config()

    # Init data providers
    dataProviderManager.setup_data_providers()

    # Init export methods
    exportUtils.load_export_methods()

    # Init widget configurations
    widgetConfUtils.setup_widget_configurations()

    # Init layouts
    layoutsUtils.setup_layouts()
