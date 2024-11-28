import os

from debiaiServer.debiai_gui_utils import data_folder_path

from debiaiServer.modules.dataProviders import (
    dataProviderManager,
)
from debiaiServer.modules.exportMethods import (
    exportUtils,
)
from debiaiServer.modules.algoProviders import (
    algoProvidersManager,
)
from debiaiServer.utils.widgetConfigurations import (
    widgetConfigurations as widgetConfUtils,
)
from debiaiServer.utils.layouts import (
    layouts as layoutsUtils,
)
from debiaiServer.config import (
    init_config as config,
)


def init():
    # Create the folder if it does not exist
    os.makedirs(data_folder_path, exist_ok=True)

    # Init config file
    config.init_config()

    # Init data providers
    dataProviderManager.setup_data_providers()

    # Init AlgoProviders
    algoProvidersManager.setup_algo_providers()

    # Init export methods
    exportUtils.load_export_methods()

    # Init widget configurations
    widgetConfUtils.setup_widget_configurations()

    # Init layouts
    layoutsUtils.setup_layouts()
