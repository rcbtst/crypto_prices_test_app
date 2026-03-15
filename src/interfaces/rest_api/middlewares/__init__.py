from fastapi import FastAPI

from src.interfaces.rest_api.middlewares.correlation_id import (
    correlation_id_middleware,
)
from src.interfaces.rest_api.middlewares.logging import LoggingMiddleware


def setup_middlewares(app: FastAPI):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(correlation_id_middleware)
