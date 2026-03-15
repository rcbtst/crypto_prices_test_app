from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

LoggerContextToken = Any


class ILogger(ABC):
    @abstractmethod
    def debug(self, message: str, context: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def info(self, message: str, context: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, context: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, context: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def exception(self, message: str, context: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def with_context(self, context: dict[str, Any]) -> ILogger:
        pass

    @abstractmethod
    def with_name(self, name: str) -> ILogger:
        pass

    @abstractmethod
    def push_context(self, context: dict[str, Any]) -> LoggerContextToken:
        pass

    @abstractmethod
    def reset_context(self, token: LoggerContextToken) -> None:
        pass
