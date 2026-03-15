from typing import Annotated, TypeAlias

from fastapi import Depends, Request

from src.application.ports import ILogger


def get_logger(request: Request) -> ILogger:
    return getattr(request.state, "logger", request.app.state.logger)


LoggerDep: TypeAlias = Annotated[ILogger, Depends(get_logger)]
