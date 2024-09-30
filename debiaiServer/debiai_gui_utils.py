import errno
import os
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
    parser.add_argument("path", nargs='?', help="The path to the DebiAI data folder.")
    parser.add_argument(
        "--port", type=int, default=PORT, help="Port on which to run the DebiAI GUI"
    )
    parser.add_argument(
        "--version", action="store_true", help="Prints the version number of DebiAI"
    )
    return parser.parse_args()

def create_folder(path=None):
    """Creates a folder at the specified path.

    Args:
        path (str, optional): The path to create the folder. If None, the current
            directory is used.

    Returns:
        str: The full path of the created folder.
    """

    if path is None:
        path = os.getcwd()

    try:
        # Check if the folder already exists
        if os.path.exists(path):
            print(f"Folder '{path}' already exists.")
            return os.path.abspath(path)  # Return the existing full path

        create_folder_answer = input("Do you want to create it ? (Y/n)")
        if create_folder_answer == "Y":
            # Create the folder
            os.makedirs(path)
            print(f"DebiAI data folder '{path}' created successfully.")
        else:
            print("end of run")
            exit()

    except OSError as e:
        if e.errno == errno.EEXIST:
            # Folder already exists, handle gracefully
            print(f"Folder '{path}' already exists.")
            return os.path.abspath(path)  # Return the full existing path
        else:
            # Other error occurred, raise exception
            raise e

    return os.path.abspath(path)

def bash_info():
    print(
        colored("Usage: ", DEBUG_COLOR) + "debiai_gui [OPTIONS] COMMAND DATA_PATH\n\n"
        "\t"
        "Use the line below to run the app: \n\n"
        "\t\t"
        "$ debiai_gui"
        + colored(" start")
        + colored(" ./debiai_data\n\n")
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
        if args.path is None:
            default_folder_name = "debiai_data"
            default_folder = os.path.join(os.getcwd(),default_folder_name)
            data_folder_path_input = input(f"Enter the path to create the DebiAI data folder ({default_folder}): ")
            if data_folder_path_input == '': 
                data_folder_path_input = default_folder
            print(f"Data folder path input :",data_folder_path_input)
            data_folder_path = os.path.abspath(data_folder_path_input)
        else:
            data_folder_path = os.path.abspath(args.path)
        data_folder_path_created = create_folder(data_folder_path)
        print(f"Data folder path:",data_folder_path_created)
        Timer(1, lambda: open_browser(args.port)).start()
        start_server(args.port, reloader=False, is_dev=False)
    else:
        bash_info()
