from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from starlette.types import ASGIApp

REQUEST_ID_HEADER = "X-Request-ID"


def correlation_id_middleware(app: ASGIApp) -> ASGIApp:
    return CorrelationIdMiddleware(
        app,
        header_name=REQUEST_ID_HEADER,
        generator=lambda: uuid4().hex,
        validator=None,
    )
