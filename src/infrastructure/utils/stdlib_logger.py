from __future__ import annotations

import logging
from contextvars import ContextVar, Token
from typing import ClassVar

from src.application.ports import ILogger


class StdLibLogger(ILogger):
    _context_stack: ClassVar[ContextVar[tuple[dict[str, object], ...]]] = ContextVar(
        "stdlib_logger_context_stack",
        default=(),
    )

    def __init__(
        self,
        logger_name: str | None = None,
        base_context: dict[str, object] | None = None,
    ):
        self._logger = logging.getLogger(logger_name or __name__)
        self._base_context = base_context or {}

    def debug(self, message: str, context: dict[str, object] | None = None) -> None:
        self._logger.debug(self._format_message(message, context))

    def info(self, message: str, context: dict[str, object] | None = None) -> None:
        self._logger.info(self._format_message(message, context))

    def warning(self, message: str, context: dict[str, object] | None = None) -> None:
        self._logger.warning(self._format_message(message, context))

    def error(self, message: str, context: dict[str, object] | None = None) -> None:
        self._logger.error(self._format_message(message, context))

    def exception(self, message: str, context: dict[str, object] | None = None) -> None:
        self._logger.exception(self._format_message(message, context))

    def with_context(self, context: dict[str, object]) -> StdLibLogger:
        return StdLibLogger(
            logger_name=self._logger.name,
            base_context={**self._base_context, **context},
        )

    def with_name(self, name: str) -> StdLibLogger:
        return StdLibLogger(logger_name=name, base_context=self._base_context)

    def push_context(
        self, context: dict[str, object]
    ) -> Token[tuple[dict[str, object], ...]]:
        stack_var = type(self)._context_stack
        stack = stack_var.get()
        token = stack_var.set(stack + (context,))
        return token

    def reset_context(self, token: Token[tuple[dict[str, object], ...]]) -> None:
        type(self)._context_stack.reset(token)

    def _get_global_context(self) -> dict[str, object]:
        global_context: dict[str, object] = {}
        for ctx in type(self)._context_stack.get():
            global_context.update(ctx)
        return global_context

    def _format_message(
        self,
        message: str,
        context: dict[str, object] | None = None,
    ) -> str:
        merged_context = {
            **self._get_global_context(),
            **self._base_context,
            **(context or {}),
        }
        if merged_context:
            ctx_str = " | ".join(f"{k}={v}" for k, v in merged_context.items())
            return f"{message} [{ctx_str}]"
        return message
