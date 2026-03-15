from src.application.contracts.get_ticker_last_record import (
    GetTickerLastRecordCommand,
    GetTickerLastRecordResult,
)
from src.application.dtos import TickerDataDTO
from src.application.exceptions import UseCaseError
from src.application.ports import ILogger, ITransactionManager
from src.application.use_cases.base import IUseCase


class FailedToGetLastTickerRecord(UseCaseError):
    pass


class GetTickerLastRecordUseCase(
    IUseCase[GetTickerLastRecordCommand, GetTickerLastRecordResult]
):
    def __init__(
        self,
        logger: ILogger,
        transaction_manager: ITransactionManager,
    ):
        self._logger = logger.with_name(__name__)
        self._transaction_manager = transaction_manager

    async def execute(
        self, command: GetTickerLastRecordCommand
    ) -> GetTickerLastRecordResult:
        use_case_logger = self._logger.with_context(command.safe_dump())
        use_case_logger.info("Getting ticker last record")

        try:
            async with self._transaction_manager as tm:
                last_ticker_record = await tm.tickers_data.get_last(command.ticker_name)

            result = GetTickerLastRecordResult(
                result=TickerDataDTO.model_validate(
                    last_ticker_record, from_attributes=True
                )
                if last_ticker_record
                else None,
            )
        except Exception as e:
            use_case_logger.exception("Failed to get last ticker record")
            raise FailedToGetLastTickerRecord from e

        use_case_logger.info(
            "Last ticker record fetched successfully",
            context={"records_exists": bool(result.result)},
        )

        return result
