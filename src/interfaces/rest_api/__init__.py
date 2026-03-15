from asgi_correlation_id import correlation_id
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler

from src.infrastructure.di_config import ApplicationContainer
from src.interfaces.rest_api.middlewares import setup_middlewares
from src.interfaces.rest_api.middlewares.correlation_id import REQUEST_ID_HEADER
from src.interfaces.rest_api.routes import setup_routes


class WebApiApp(FastAPI):
    container: ApplicationContainer


def setup_app() -> WebApiApp:
    container = ApplicationContainer()
    container.wire(packages=[__name__])

    app = WebApiApp(title="Test API")
    app.container = container
    app.state.logger = container.logger().with_name(__name__)

    setup_middlewares(app)
    setup_routes(app)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger = getattr(request.state, "logger", request.app.state.logger)
    logger.exception("API Unhandled exception")
    return await http_exception_handler(
        request,
        HTTPException(
            500,
            "Internal server error",
            headers={REQUEST_ID_HEADER: correlation_id.get() or ""},
        ),
    )


__all__ = ["WebApiApp", "setup_app"]
