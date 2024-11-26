import errno
import os
import argparse
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
from threading import Timer
from termcolor import colored
from debiaiServer.config.init_config import DEBUG_COLOR, SUCCESS_COLOR

import sys

sys.stdout.reconfigure(encoding="utf-8")

data_folder_path = "debiai_data"  # The path to the DebiAI data folder
DEFAULT_PORT = 3000  # default port

welcome_logo = """
                                                    █████████████            
                                                 ███████████████████         
                                               ███████████████████████       
                                             ██████████████████████████      
   █████████             ████        ███    ██████████   ██████   ███████    
    ███    ███            ███              ██████████     █████   ████████   
    ███     ███  ███████  ████████  ████   █████████   █   ████   ████████   
    ███     ███ ███   ███ ███   ███  ███   ████████   ███   ███   ████████   
    ███     ███ ████████  ███   ███  ███   ███████           ██   ████████   
    ███    ███  ███       ███   ███  ███   ███████   █████   ██   ████████   
   ██████████    ███████  ████████  █████  ██████   ███████   █   ███████    
                                            █████████████████████████████    
                                             ██████████████████████████      
                                            ██████████████████████████       
                                           █████████████████████████         
                                         ██████     █████████████            
                                       ██████                                
                                      ████                                   
"""


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


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
            # Check if the path is a folder
            if not os.path.isdir(path):
                raise OSError(
                    errno.ENOTDIR,
                    f"'{path}' is not a folder. Please provide a valid folder path.",
                )
            return os.path.abspath(path)  # Return the existing full path

        # If the folder does not exist, ask the user if they want to create it
        create_folder_answer = gather_user_input(
            "The folder does not exist. Do you want to create it? (Y/n): "
        )
        if create_folder_answer == "Y" or create_folder_answer == "":
            # Create the folder
            os.makedirs(path)
            print(f"DebiAI data folder '{path}' created successfully.")
        else:
            print("Folder creation cancelled, exiting.")
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


def gather_user_input(message):
    try:
        user_input = input(message)
        return user_input
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit()


def bash_info():
    print(
        colored("Usage: ", DEBUG_COLOR) + "debiai-gui [OPTIONS] COMMAND DATA_PATH\n\n"
        "\t"
        "Use the line below to run the app: \n\n"
        "\t\t"
        "$ debiai-gui"
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


def run(start=False):
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Run the DebiAI GUI")
    parser.add_argument("command", nargs="?", help="Start the DebiAI GUI server")
    parser.add_argument("path", nargs="?", help="The path to the DebiAI data folder.")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port on which to run the DebiAI GUI, default is " + str(DEFAULT_PORT),
    )
    parser.add_argument(
        "--version", action="store_true", help="Prints the version number of DebiAI"
    )
    args = parser.parse_args()

    # Check the arguments
    if args.version:
        # Print the version number
        from debiaiServer.utils.utils import get_app_version

        version = get_app_version()
        print("DebiAI Version:" + colored(version, SUCCESS_COLOR))

    elif args.command == "start" or start:
        global data_folder_path

        print(welcome_logo)
        print("   Welcome!\n")

        # Deal with the data folder path
        if args.path is None:
            # Set the default data folder path
            default_folder_name = "debiai_data"
            default_folder = os.path.join(os.getcwd(), default_folder_name)

            # Ask the user for the data folder path
            print("DebiAI requires a data folder to store the data.")
            data_folder_path_input = gather_user_input(
                f"Enter the path of the DebiAI data folder ({default_folder}): "
            )
            if data_folder_path_input == "":
                data_folder_path_input = default_folder
            print("Data folder path input :", data_folder_path_input)
            data_folder_path = os.path.abspath(data_folder_path_input)
        else:
            # Use the provided data folder path
            data_folder_path = os.path.abspath(args.path)

        # Create the data folder
        data_folder_path_created = create_folder(data_folder_path)
        print("Data folder path:", data_folder_path_created, "\n")

        # Start the DebiAI GUI
        animation = Loader("Starting the DebiAI GUI", "")
        animation.start()
        start_server_with_browser(args.port, animation)

    else:
        # Print the usage information
        bash_info()


def start_server_with_browser(port, animation):
    from debiaiServer.websrv import start_server, open_browser

    Timer(1, lambda: open_browser(port)).start()
    animation.stop()
    start_server(port, reloader=False, is_dev=False)
