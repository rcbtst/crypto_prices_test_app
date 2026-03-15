from src.application.contracts.base import NoneResult
from src.application.contracts.update_ticker_data import UpdateTickerDataCommand
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITickerDataFetcher, ITransactionManager
from src.application.use_cases.base import IUseCase
from src.domain.entities import TickerData


class FailedToUpdateTickerData(UseCaseError):
    pass


class UpdateTickerDataUseCase(IUseCase[UpdateTickerDataCommand, NoneResult]):
    def __init__(
        self,
        logger: ILogger,
        transaction_manager: ITransactionManager,
        ticker_data_fetcher: ITickerDataFetcher,
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager
        self._ticker_data_fetcher = ticker_data_fetcher

    async def execute(self, command: UpdateTickerDataCommand) -> NoneResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Updating ticker data")

        try:
            fetched_ticker_data = await self._ticker_data_fetcher.fetch_new_ticker_data(
                command.ticker_name
            )

            new_ticker_data = TickerData(
                name=fetched_ticker_data.name,
                price=fetched_ticker_data.price,
                timestamp=fetched_ticker_data.timestamp,
            )

            async with self._transaction_manager as tm:
                await tm.tickers_data.save(new_ticker_data)

        except Exception as e:
            use_case_logger.exception("Failed to update ticker data")
            raise FailedToUpdateTickerData from e

        use_case_logger.info("Ticker data updated successfully")

        return NoneResult()
