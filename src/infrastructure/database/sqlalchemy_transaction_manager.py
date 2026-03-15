from __future__ import annotations

from typing import Callable, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports import ILogger, ITransactionManager
from src.domain.repositories import ITickerDataRepository
from src.infrastructure.database.mappers import SQLAlchemyTickerDataMapper
from src.infrastructure.database.repositories import SQLAlchemyTickerDataRepository
from src.infrastructure.database.schema import TickerData


class SQLAlchemyTransactionManager(ITransactionManager):
    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        logger: ILogger,
    ):
        self.session_factory = session_factory
        self._logger = logger.with_name(__name__)

    async def __aenter__(self) -> SQLAlchemyTransactionManager:
        self._logger.debug("Starting database transaction")

        try:
            self.session: AsyncSession = self.session_factory()

            self.tickers_data: ITickerDataRepository = SQLAlchemyTickerDataRepository(
                self.session, SQLAlchemyTickerDataMapper(), TickerData, self._logger
            )

            await self.session.begin()

            return self
        except Exception:
            self._logger.exception("Failed to start database transaction")
            raise

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        try:
            if exc_type is None:
                self._logger.debug("Committing database transaction")
                await self.session.commit()
                self._logger.debug("Database transaction committed successfully")
            else:
                self._logger.warning(
                    "Rolling back database transaction",
                    context={
                        "exception_type": exc_type.__name__ if exc_type else None,
                        "exception_message": str(exc_value) if exc_value else None,
                    },
                )
                await self.session.rollback()
                self._logger.debug("Database transaction rolled back")
        except Exception:
            self._logger.exception("Error during db transaction cleanup")
            raise
        finally:
            await self.session.close()
            self._logger.debug("Database session closed")
