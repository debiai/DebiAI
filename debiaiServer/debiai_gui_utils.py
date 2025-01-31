import os
import sys
import errno
import argparse
from threading import Timer
from termcolor import colored
from debiaiServer.config.init_config import DEBUG_COLOR, SUCCESS_COLOR
from debiaiServer.utils.utils import Loader

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


def create_folder(path=None):
    """Creates a folder at the specified path."""
    path = path or os.getcwd()

    # Return the absolute path if the folder already exists
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise OSError(
                errno.ENOTDIR,
                f"'{path}' is not a folder. Please provide a valid folder path.",
            )
        return os.path.abspath(path)

    # Create the folder if it does not exist
    create_folder_answer = gather_user_input(
        f"The folder {path} does not exist. Create it? (Y/n): "
    )
    if create_folder_answer.lower() in ("y", ""):
        os.makedirs(path)
        print(f"DebiAI data folder '{path}' created successfully.")
    else:
        print("Folder creation cancelled, exiting.")
        exit()

    return os.path.abspath(path)


def gather_user_input(message):
    try:
        return input(message)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        exit()


def setup_data_folder(arg_path):
    global data_folder_path

    if arg_path:
        data_folder_path = create_folder(arg_path)
    else:
        print("DebiAI requires a folder to store the data.")
        data_folder_path = create_folder(
            gather_user_input(f"Enter data folder path ({data_folder_path}): ")
            or data_folder_path
        )
        print("use --data-folder to specify the data folder path")
    print("Data folder path:", data_folder_path, "\n")


def debiai_gui_start(path, port):
    # Display welcome message
    print(welcome_logo)
    print("   Welcome!\n")

    # Ask for the data folder path
    setup_data_folder(path)

    # Start the DebiAI GUI
    start_loading_animation = Loader("Starting the DebiAI GUI", "")
    start_loading_animation.start()
    from debiaiServer.websrv import start_server, open_browser

    Timer(1, lambda: open_browser(port)).start()
    start_loading_animation.stop()
    start_server(port, reloader=False, is_dev=False)


def main():
    parser = argparse.ArgumentParser(
        description="""DebiAI GUI Command Line. 
Learn more about DebiAI at https://debiai.irt-systemx.fr/""",
        add_help=True,
    )

    # Version and help
    parser.add_argument(
        "-v", "--version", action="store_true", help="Print DebiAI version number"
    )

    # Start command
    subparsers = parser.add_subparsers(
        dest="command", title="Command", help="Start the DebiAI GUI", metavar="start"
    )
    start_parser = subparsers.add_parser("start")
    start_parser.add_argument(
        "-d", "--data-folder", type=str, help="Path to the data folder"
    )
    start_parser.add_argument(
        "-p", "--port", type=int, default=DEFAULT_PORT, help="Port to run the server on"
    )

    # Parse the arguments
    args = parser.parse_args()
    if args.version:
        from debiaiServer.utils.utils import get_app_version

        print("DebiAI Version:", colored(get_app_version(), SUCCESS_COLOR))
    elif args.command == "start":
        debiai_gui_start(args.data_folder, args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
