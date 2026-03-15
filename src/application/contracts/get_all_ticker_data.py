from src.application.contracts.base import Command, Result
from src.application.dtos import TickerDataDTO


class GetAllTickerDataCommand(Command):
    ticker_name: str


class GetAllTickerDataResult(Result):
    result: list[TickerDataDTO]
