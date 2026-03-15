from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.entities.ticker_data import TickerData
from src.domain.repositories.base import IRepository


class ITickerDataRepository(IRepository[TickerData], ABC):
    @abstractmethod
    async def get_all(self, ticker_name: str) -> list[TickerData]:
        """Get all ticker data entities for provided ticker name"""
        pass

    @abstractmethod
    async def get_last(self, ticker_name: str) -> TickerData | None:
        """Get last ticker data entity record for provided ticker name, or None if it's not exist"""
        pass

    @abstractmethod
    async def get_all_filtered_by_date(
        self,
        ticker_name: str,
        min_date: datetime | None = None,
        max_date: datetime | None = None,
    ) -> list[TickerData]:
        """Get all ticker data entities for provided ticker name filtered by date range"""
        pass
