# This file is used to run the debiai-gui server in development mode

from debiaiServer import websrv

websrv.start_server(port=3000, reloader=True, is_dev=True)
