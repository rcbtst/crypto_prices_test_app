from datetime import datetime

from sqlalchemy import select

from src.domain.entities import TickerData
from src.domain.repositories import ITickerDataRepository
from src.infrastructure.database.repositories.sqlalchemy_repository import (
    SQLAlchemyRepository,
)
from src.infrastructure.database.schema import TickerData as TickerDataORM


class SQLAlchemyTickerDataRepository(
    SQLAlchemyRepository[TickerDataORM, TickerData], ITickerDataRepository
):
    async def get_all(self, ticker_name: str) -> list[TickerData]:
        logger = self._logger.with_context({"ticker_name": ticker_name})
        logger.debug("Getting all ticker data from db")

        try:
            result = await self.session.scalars(
                select(TickerDataORM)
                .where(TickerDataORM.name == ticker_name)
                .order_by(TickerDataORM.timestamp.desc())
            )

            result = list(result.all())

            return [self.mapper.to_domain(item) for item in result]
        except Exception:
            logger.exception("Failed to get all ticker data from db")
            raise

    async def get_last(self, ticker_name: str) -> TickerData | None:
        logger = self._logger.with_context({"ticker_name": ticker_name})
        logger.debug("Getting last ticker record from db")

        try:
            result = await self.session.scalar(
                select(TickerDataORM)
                .where(TickerDataORM.name == ticker_name)
                .order_by(TickerDataORM.timestamp.desc())
                .limit(1)
            )

            if not result:
                return None

            return self.mapper.to_domain(result)
        except Exception:
            logger.exception("Failed to get last ticker record from db")
            raise

    async def get_all_filtered_by_date(
        self,
        ticker_name: str,
        min_date: datetime | None = None,
        max_date: datetime | None = None,
    ) -> list[TickerData]:
        logger = self._logger.with_context(
            {
                "ticker_name": ticker_name,
                "min_date": str(min_date),
                "max_date": str(max_date),
            }
        )
        logger.debug("Getting all filtered by date ticker data from db")

        try:
            query = select(TickerDataORM).where(TickerDataORM.name == ticker_name)

            if min_date:
                query = query.where(
                    TickerDataORM.timestamp >= int(min_date.timestamp())
                )

            if max_date:
                query = query.where(
                    TickerDataORM.timestamp <= int(max_date.timestamp())
                )

            result = await self.session.scalars(
                query.order_by(TickerDataORM.timestamp.desc())
            )

            result = list(result.all())

            return [self.mapper.to_domain(item) for item in result]
        except Exception:
            logger.exception("Failed to get all filtered by date ticker data from db")
            raise
