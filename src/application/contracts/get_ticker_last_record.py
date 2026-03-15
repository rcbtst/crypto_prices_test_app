from src.application.contracts.base import Command, Result
from src.application.dtos import TickerDataDTO


class GetTickerLastRecordCommand(Command):
    ticker_name: str


class GetTickerLastRecordResult(Result):
    result: TickerDataDTO | None = None
