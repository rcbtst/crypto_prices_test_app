from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import URL

from src.application.ports import ILogger


class SQLAlchemyDatabase:
    def __init__(self, url: str | URL, logger: ILogger, **engine_kwargs: dict) -> None:
        self._logger = logger.with_name(__name__)
        self._logger.debug("Creating SQLAlchemy engine")

        self._engine = create_async_engine(url, **engine_kwargs)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def dispose(self) -> None:
        self._logger.debug("Disposing SQLAlchemy engine")
        await self._engine.dispose()
