from abc import ABC, abstractmethod

from src.application.dtos import TickerDataDTO


class ITickerDataFetcher(ABC):
    @abstractmethod
    async def fetch_new_ticker_data(self, ticker_name: str) -> TickerDataDTO:
        pass
