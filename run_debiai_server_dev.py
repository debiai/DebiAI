# This file is used to run the debiai-gui server in development mode

from debiaiServer.websrv import stop_server


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "debiaiServer.websrv:start_server_dev",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info",
        factory=True,
    )
    stop_server()
