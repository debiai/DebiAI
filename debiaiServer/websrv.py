import os
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from termcolor import colored
from debiaiServer.init import init
from debiaiServer.utils.utils import get_app_version
from debiaiServer.config.init_config import DEBUG_COLOR

DEV_FRONTEND_URL = "http://localhost:8080/"
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files in production
if not os.path.exists("dist"):
    os.makedirs("dist")
app.mount("/static", StaticFiles(directory="dist"), name="static")


def send_frontend(path: str, is_dev: bool):
    if path == "/":
        path = "index.html"

    # If production, serve the "dist" folder
    if not is_dev:
        file_path = os.path.join("dist", path)
        if os.path.exists(file_path):
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")

    # In development, proxy requests to the DEV_FRONTEND_URL
    else:
        try:
            resp = requests.get(f"{DEV_FRONTEND_URL}{path}")
            return JSONResponse(
                content=resp.content.decode("utf-8"),
                status_code=resp.status_code,
                headers=dict(resp.headers),
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return JSONResponse(
                content={
                    "error": f"You are in a development environment and the DebiAI frontend is not available at {DEV_FRONTEND_URL}"
                },
                status_code=503,
            )


@app.get("/{path:path}")
async def serve_frontend(path: str, request: Request):
    is_dev = request.headers.get("X-Environment", "development") == "development"
    return send_frontend(path, is_dev)


@app.get("/")
async def serve_index(request: Request):
    is_dev = request.headers.get("X-Environment", "development") == "development"
    return send_frontend("/", is_dev)


def start_server(
    port: int,
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
        "   DebiAI is available at " + colored(f"http://localhost:{port}", DEBUG_COLOR)
    )

    # Start the FastAPI server
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=reloader,
        log_level="info",
    )

    # Print goodbye message
    print("\n\n  Goodbye!")
    print("Thank you for using DebiAI.\n")


if __name__ == "__main__":
    start_server(port=3000, reloader=False, is_dev=True)
