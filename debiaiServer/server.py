from threading import Timer
import sys
from debiaiServer.websrv import start_server, open_browser
from debiaiServer.utils.utils import get_app_version

BRIGHT_CYAN = "\033[96m"
BRIGHT_GREEN = "\033[92m"
RESET = "\033[0m"


def print_bash_info():
    print(
        f"{BRIGHT_CYAN}Usage:{RESET} debiai-gui [OPTIONS] COMMAND\n\n"
        "\t"
        "Use the line below to run the app: \n\n"
        "\t\t"
        "$ debiai-gui"
        f"{BRIGHT_GREEN} start{RESET}\n\n"
        f"{BRIGHT_CYAN}Options:{RESET}\n"
        "\t"
        f"{BRIGHT_GREEN}--version {RESET} Prints DebiAI version number.\n"
        f"{BRIGHT_CYAN}Commands:{RESET}\n"
        "\t"
        f"{BRIGHT_GREEN}start {RESET}     Starts the DebiAI GUI and open it in a web browser.\n"
    )


def run():
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            Timer(1, open_browser).start()
            start_server(reloader=False)
        elif sys.argv[1] == "--version":
            version = get_app_version()
            print("DebiAI Version:" f"{BRIGHT_GREEN}{version}{RESET}")
        else:
            print_bash_info()
    else:
        print_bash_info()
