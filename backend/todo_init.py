import dataProviders.dataProviders as dataProviders
import export.exportUtils as exportUtils
import config.configUtil as configUtil

def init():
    # Init config file
    configUtil.init_config()

    # Init data providers
    dataProviders.setup_data_prividers()

    # Init export methods
    exportUtils.load_export_methods()