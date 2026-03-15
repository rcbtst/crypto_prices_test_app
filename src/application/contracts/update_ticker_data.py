from src.application.contracts.base import Command


class UpdateTickerDataCommand(Command):
    ticker_name: str
