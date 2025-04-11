# This file is used to run the debiai-gui server in production mode

from debiaiServer.websrv import start_server_prod

if __name__ == "__main__":
    start_server_prod(port=3000)
