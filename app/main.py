from fastapi import FastAPI

from .api import router as api_router

APP_VERSION = "0.1.0-mvp"

app = FastAPI(title="GeoWar Pulse API", version=APP_VERSION)
app.include_router(api_router)


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "GeoWar Pulse backend is running", "version": APP_VERSION}
