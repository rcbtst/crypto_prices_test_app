from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Optional, Type

from src.domain.repositories import ITickerDataRepository


class ITransactionManager(AbstractAsyncContextManager["ITransactionManager"], ABC):
    tickers_data: ITickerDataRepository

    @abstractmethod
    async def __aenter__(self) -> ITransactionManager:
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        pass
