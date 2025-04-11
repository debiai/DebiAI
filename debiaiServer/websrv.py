import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from termcolor import colored
from debiaiServer.init import init
from debiaiServer.utils.utils import get_app_version, SuppressLogsMiddleware
from debiaiServer.config.init_config import DEBUG_COLOR
from debiaiServer.controller.projects import router as projects_router

FRONTEND_DIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the projects router
app.include_router(projects_router, prefix="/api")

# Set the logger middleware
app.add_middleware(SuppressLogsMiddleware)


def send_frontend(path: str):
    if path == "/":
        path = "index.html"

    # For production, serve the "dist" folder
    file_path = os.path.join(FRONTEND_DIST_PATH, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


def start_server(port: int, data_folder_path: str = None, parameters: dict = {}):
    # Run DebiAI init
    print("================= DebiAI " + get_app_version() + " ====================")
    init(data_folder_path, parameters)
    print("======================== RUN =======================")
    print(
        "   DebiAI is available at " + colored(f"http://localhost:{port}", DEBUG_COLOR)
    )


def start_server_dev():
    start_server(port=3000)
    return app


def stop_server():
    # Print goodbye message
    print("\n\n  Goodbye!")
    print("Thank you for using DebiAI.\n")


def start_server_prod(
    port: int = 3000, data_folder_path: str = None, parameters: dict = {}
):
    start_server(port, data_folder_path, parameters)

    # Serve static files in production
    app.mount("/static", StaticFiles(directory=FRONTEND_DIST_PATH), name="static")

    # Serve the frontend files
    @app.get("/")
    async def serve_index():
        return send_frontend("/")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        return send_frontend(path)

    import uvicorn

    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

    stop_server()


if __name__ == "__main__":
    raise Exception(
        "This file is not meant to be run directly. Use the\
 `debiai/run_debiai_server_dev.py` script instead."
    )
