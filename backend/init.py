import dataProviders.dataProviderManager as dataProviderManager
import exportMethods.exportUtils as exportUtils
import config.init_config as config


def init():
    # Init config file
    config.init_config()

    # Init data providers
    dataProviderManager.setup_data_providers()

    # Init export methods
    exportUtils.load_export_methods()
