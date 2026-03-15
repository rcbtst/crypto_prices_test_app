from fastapi import FastAPI

from src.interfaces.rest_api.routes.health import router as health_router
from src.interfaces.rest_api.routes.tickers import router as tickers_router


def setup_routes(app: FastAPI):
    app.include_router(health_router)
    app.include_router(tickers_router)
