import os
import sys
import errno
import argparse
import webbrowser
from threading import Timer
from termcolor import colored
from debiaiServer.config.init_config import SUCCESS_COLOR
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


def open_browser(port):
    # Check if the browser is open
    is_browser_open = False
    try:
        webbrowser.get()
        is_browser_open = True
    except webbrowser.Error:
        pass

    # Open the browser
    try:
        url = f"http://localhost:{port}"
        if is_browser_open:
            webbrowser.open_new_tab(url)
        else:
            webbrowser.open(url)
    except webbrowser.Error:
        print(
            colored(
                "Unable to open the browser. Please open your browser and go to " + url,
                "red",
            )
        )


def debiai_gui_start(path, port, no_browser=False, data_providers=[]):
    # Display welcome message
    print(welcome_logo)
    print("   Welcome!\n")

    # Ask for the data folder path
    setup_data_folder(path)

    # Import the DebiAI GUI with a loading animation
    start_loading_animation = Loader("Starting the DebiAI GUI", "")
    start_loading_animation.start()
    from debiaiServer.websrv import start_server

    start_loading_animation.stop()

    # Open the browser with a little delay
    if not no_browser:
        Timer(0.5, open_browser, args=[port]).start()

    # Start the DebiAI GUI
    start_server(
        port=port,
        data_providers=data_providers,
        reloader=False,
        is_dev=False,
    )


def main():
    parser = argparse.ArgumentParser(
        description="""DebiAI GUI Command Line.
Learn more about DebiAI at https://debiai.irt-systemx.fr/"""
    )

    # Version flag
    parser.add_argument(
        "-v", "--version", action="store_true", help="Print DebiAI version number"
    )

    # Commands
    subparsers = parser.add_subparsers(
        dest="command",
        title="DebiAI-GUI",
        help="Available commands",
        metavar="[command]",
    )

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the DebiAI GUI")
    start_parser.add_argument(
        "-d",
        "--data-folder",
        type=str,
        help="Path to the data folder",
    )
    start_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port to run the server on",
    )
    start_parser.add_argument(
        "-nb",
        "--no-browser",
        action="store_true",
        help="Do not open the browser on startup",
    )
    start_parser.add_argument(
        "-dp",
        "--data-provider",
        type=str,
        nargs="+",  # 1 or more arguments
        help="One or more data provider URLs",
    )

    # Parse the arguments
    args = parser.parse_args()
    if args.version:
        from debiaiServer.utils.utils import get_app_version

        print("DebiAI Version:", colored(get_app_version(), SUCCESS_COLOR))
    elif args.command == "start":
        debiai_gui_start(
            path=args.data_folder,
            port=args.port,
            no_browser=args.no_browser,
            data_providers=args.data_provider,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
