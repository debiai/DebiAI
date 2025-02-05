import requests
import connexion
from flask_cors import CORS
from waitress import serve
from termcolor import colored
from debiaiServer.init import init
from debiaiServer.utils.utils import get_app_version
from debiaiServer.config.init_config import DEBUG_COLOR
from flask import send_from_directory, request, Response


DEV_FRONTEND_URL = "http://localhost:8080/"
app = connexion.App(__name__)
app.add_api("swagger.yaml", strict_validation=True)
CORS(app.app)


def send_frontend(path, is_dev):
    if path == "/":
        path = "index.html"

    # If production, use the index.html from the dist folder
    if not is_dev:
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


def create_app(is_dev):
    # For serving the dashboard
    @app.route("/")
    def send_index():
        return send_frontend("/", is_dev)

    # For serving the dashboard assets
    @app.route("/<path:path>")
    def send_supporting_elements(path):
        return send_frontend(path, is_dev)

    return app


def start_server(
    port,
    data_folder_path: str = None,
    parameters: dict = {},
    reloader: bool = True,
    is_dev: bool = True,
):
    # Run DebiAI init
    print("================= DebiAI " + get_app_version() + " ====================")
    init(data_folder_path, parameters)
    print("======================== RUN =======================")
    print(
        "   DebiAI is available at "
        + colored("http://localhost:" + str(port), DEBUG_COLOR)
    )
    app = create_app(is_dev)

    if is_dev:
        # Use flask server for development
        app.run(port, debug=True, host="0.0.0.0", use_reloader=reloader)
    else:
        # Use waitress for production
        try:
            serve(app, host="0.0.0.0", port=port, threads=6)
        except OSError:
            print(
                colored(
                    f"Port {port} is already in use. Please try another port.", "red"
                )
            )

    # Print goodbye message
    print("\n\n  Goodbye!")
    print("Thank you for using DebiAI.\n")


if __name__ == "__main__":
    start_server(port=3000, reloader=False, is_dev=True)
