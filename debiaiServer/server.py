from threading import Timer
import sys
from debiaiServer.websrv import start_server, open_browser


def run():
    Timer(1, open_browser).start()
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_server(reloader=False)
    else:
        print("Invalid command. Use 'debiai-gui start'")
