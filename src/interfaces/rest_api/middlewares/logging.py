from collections.abc import Awaitable, Callable
from time import perf_counter

from asgi_correlation_id import correlation_id
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.application.ports import ILogger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = correlation_id.get()

        logger: ILogger = request.app.state.logger
        request_context = {
            "fastapi_context": {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            }
        }
        request_context_token = logger.push_context(request_context)
        request.state.logger = logger

        logger.info("API Request received")
        start_time = perf_counter()
        try:
            response = await call_next(request)
        except:
            logger.exception(
                "API Request failed",
                context={"processing_time": round(perf_counter() - start_time, 4)},
            )
            raise
        else:
            logger.info(
                "API Request completed",
                context={
                    "processing_time": round(perf_counter() - start_time, 4),
                    "status_code": response.status_code,
                },
            )
        finally:
            logger.reset_context(request_context_token)

        return response
