import argparse
from threading import Timer
from termcolor import colored
from debiaiServer.utils.utils import get_app_version
from debiaiServer.websrv import start_server, open_browser
from debiaiServer.config.init_config import DEBUG_COLOR, SUCCESS_COLOR
from debiaiServer.modules.dataProviders.pythonDataProvider.dataUtils import (
    pythonModuleUtils,
)


DATA_PATH = pythonModuleUtils.DATA_PATH
PORT = 3000  # default port


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the DebiAI GUI")
    parser.add_argument("command", nargs="?", help="Start the DebiAI GUI server")
    parser.add_argument(
        "--port", type=int, default=PORT, help="Port on which to run the DebiAI GUI"
    )
    parser.add_argument(
        "--version", action="store_true", help="Prints the version number of DebiAI"
    )
    return parser.parse_args()


def bash_info():
    print(
        colored("Usage: ", DEBUG_COLOR) + "debiai-gui [OPTIONS] COMMAND\n\n"
        "\t"
        "Use the line below to run the app: \n\n"
        "\t\t"
        "$ debiai-gui"
        + colored(" start\n\n")
        + colored("Options:\n", DEBUG_COLOR)
        + "\t"
        + colored("--version ", SUCCESS_COLOR)
        + "      Prints DebiAI version number.\n"
        + "\t"
        + colored("--port [NUMBER] ", SUCCESS_COLOR)
        + "Allows you to choose a port.\n"
        + colored("Commands:\n", DEBUG_COLOR)
        + "\t"
        + colored("start ", SUCCESS_COLOR)
        + "Starts the DebiAI GUI and open it in a web browser.\n\n"
        + "For more information visit: "
        + colored("https://debiai.irt-systemx.fr/ \n\n", None, attrs=["bold"])
    )


def run():
    args = parse_arguments()

    if args.version:
        version = get_app_version()
        print("DebiAI Version:" + colored(version, SUCCESS_COLOR))
    elif args.command == "start":
        Timer(1, lambda: open_browser(args.port)).start()
        start_server(args.port, reloader=False, is_dev=False)
    else:
        bash_info()
