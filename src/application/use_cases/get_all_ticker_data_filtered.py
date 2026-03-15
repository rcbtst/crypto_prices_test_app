from src.application.contracts.get_all_ticker_data_filtered import (
    GetAllTickerDataFilteredCommand,
    GetAllTickerDataFilteredResult,
)
from src.application.dtos import TickerDataDTO
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class FailedToGetAllTickerDataFiltered(UseCaseError):
    pass


class GetAllTickerDataFilteredUseCase(
    IUseCase[GetAllTickerDataFilteredCommand, GetAllTickerDataFilteredResult]
):
    def __init__(
        self,
        logger: ILogger,
        transaction_manager: ITransactionManager,
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    async def execute(
        self, command: GetAllTickerDataFilteredCommand
    ) -> GetAllTickerDataFilteredResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Getting all filtered ticker data")

        try:
            async with self._transaction_manager as tm:
                all_ticker_data_filtered = (
                    await tm.tickers_data.get_all_filtered_by_date(
                        command.ticker_name,
                        min_date=command.min_date,
                        max_date=command.max_date,
                    )
                )

            result = GetAllTickerDataFilteredResult(
                result=[
                    TickerDataDTO.model_validate(item, from_attributes=True)
                    for item in all_ticker_data_filtered
                ]
            )
        except Exception as e:
            use_case_logger.exception("Failed to get all filtered ticker data")
            raise FailedToGetAllTickerDataFiltered from e

        use_case_logger.info(
            "All filtered ticker data fetched successfully",
            context={"records_qty": len(result.result)},
        )

        return result
