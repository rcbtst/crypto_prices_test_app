from datetime import UTC, datetime

from src.application.dtos import TickerDataDTO
from src.application.ports import ILogger, ITickerDataFetcher
from src.infrastructure.external_apis.deribit_api_client import IDeribitAPIClient


class DeribitTickerDataFetcher(ITickerDataFetcher):
    def __init__(self, deribit_api_client: IDeribitAPIClient, logger: ILogger):
        self._deribit_api_client = deribit_api_client
        self._logger = logger.with_name(__name__)

    async def fetch_new_ticker_data(self, ticker_name: str) -> TickerDataDTO:
        logger = self._logger.with_context({"ticker_name": ticker_name})
        logger.info("Fetching new ticker data")

        try:
            async with self._deribit_api_client as client:
                result = await client.get_ticker_index_price(ticker_name)

            return TickerDataDTO(
                name=ticker_name,
                price=result.index_price,
                timestamp=int(datetime.now(tz=UTC).timestamp()),
            )
        except Exception:
            logger.exception("Failed to fetch new ticker data")
            raise
