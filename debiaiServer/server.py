from threading import Timer
from termcolor import colored
import sys
from debiaiServer.websrv import start_server, open_browser
from debiaiServer.utils.utils import get_app_version
from debiaiServer.modules.dataProviders.pythonDataProvider.dataUtils import (
    pythonModuleUtils,
)
from debiaiServer.config.init_config import DEBUG_COLOR, SUCCESS_COLOR


DATA_PATH = pythonModuleUtils.DATA_PATH


def bash_info():
    print(
        colored("Usage example:", DEBUG_COLOR) + "debiai-gui [OPTIONS] COMMAND\n\n"
        "\t"
        "Use the line below to run the app: \n\n"
        "\t\t"
        "$ debiai-gui"
        + colored(" start\n\n")
        + colored("Options:\n", DEBUG_COLOR)
        + "\t"
        + colored("--version ", SUCCESS_COLOR)
        + "Prints DebiAI version number.\n"
        + colored("Commands:\n", DEBUG_COLOR)
        + "\t"
        + colored("start ", SUCCESS_COLOR)
        + "    Starts the DebiAI GUI and open it in a web browser.\n"
    )


def run():
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            Timer(1, open_browser).start()
            start_server(reloader=False)
        elif sys.argv[1] == "--version":
            version = get_app_version()
            print("DebiAI Version:" + colored(version, SUCCESS_COLOR))
        else:
            bash_info()
    else:
        bash_info()
