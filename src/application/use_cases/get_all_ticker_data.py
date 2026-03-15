from src.application.contracts.get_all_ticker_data import (
    GetAllTickerDataCommand,
    GetAllTickerDataResult,
)
from src.application.dtos import TickerDataDTO
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class FailedToGetAllTickerData(UseCaseError):
    pass


class GetAllTickerDataUseCase(
    IUseCase[GetAllTickerDataCommand, GetAllTickerDataResult]
):
    def __init__(
        self,
        logger: ILogger,
        transaction_manager: ITransactionManager,
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    async def execute(self, command: GetAllTickerDataCommand) -> GetAllTickerDataResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Getting all ticker data")

        try:
            async with self._transaction_manager as tm:
                all_ticker_data = await tm.tickers_data.get_all(command.ticker_name)

            result = GetAllTickerDataResult(
                result=[
                    TickerDataDTO.model_validate(item, from_attributes=True)
                    for item in all_ticker_data
                ]
            )
        except Exception as e:
            use_case_logger.exception("Failed to get all ticker data")
            raise FailedToGetAllTickerData from e

        use_case_logger.info(
            "All ticker data fetched successfully",
            context={"records_qty": len(result.result)},
        )

        return result
