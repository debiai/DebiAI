import os
import sys
import psutil
import logging
import requests
import connexion
import webbrowser
from flask_cors import CORS
from termcolor import colored
from debiaiServer.init import init
from debiaiServer.utils.utils import get_app_version
from debiaiServer.config.init_config import DEBUG_COLOR
from flask import send_from_directory, request, Response


DEV_FRONTEND_URL = "http://localhost:8080/"
app = connexion.App(__name__)
app.add_api("swagger.yaml", strict_validation=True)
CORS(app.app)


def send_frontend(path):
    if path == "/":
        path = "index.html"

    # If production, use the index.html from the dist folder
    env = os.getenv("FLASK_ENV", "production")
    debug_mode = env == "production"
    if debug_mode:
        return send_from_directory("dist", path)

    # In development, redirect to the DEV_FRONTEND_URL
    else:
        if request.method == "GET":
            try:
                resp = requests.get(f"{DEV_FRONTEND_URL}{path}")
                excluded_headers = [
                    "content-encoding",
                    "content-length",
                    "transfer-encoding",
                    "connection",
                ]
                headers = [
                    (name, value)
                    for (name, value) in resp.raw.headers.items()
                    if name.lower() not in excluded_headers
                ]
                response = Response(resp.content, resp.status_code, headers)
                return response
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                return (
                    "You are in a development environment and the DebiAI frontend"
                    + "is not available at the url : "
                    + DEV_FRONTEND_URL,
                    503,
                )
        else:
            print("Unexpected request method")


def create_app():
    # For serving the dashboard
    @app.route("/")
    def send_index():
        return send_frontend("/")

    # For serving the dashboard assets
    @app.route("/<path:path>")
    def send_supporting_elements(path):
        return send_frontend(path)

    return app


def is_browser_open():
    """Check if a browser process is running."""
    browser_keywords = ["chrome", "firefox", "safari", "edge", "opera"]
    for proc in psutil.process_iter(["pid", "name"]):
        for keyword in browser_keywords:
            if keyword in proc.info["name"].lower():
                return True
    return False


def open_browser(port):
    url = f"http://localhost:{port}"
    if is_browser_open():
        webbrowser.open_new_tab(url)
    else:
        webbrowser.open(url)


def start_server(port, reloader=True):
    # Run DebiAI init
    print("================= DebiAI " + get_app_version() + " ====================")
    init()
    print("======================== RUN =======================")
    print(
        "   DebiAI is available at "
        + colored("http://localhost:" + str(port), DEBUG_COLOR)
    )

    from gevent.pywsgi import WSGIServer

    app = create_app()
    http_server = WSGIServer(("127.0.0.1", port), app)
    http_server.serve_forever()

    app.run(port, debug=True, host="0.0.0.0", use_reloader=reloader)
