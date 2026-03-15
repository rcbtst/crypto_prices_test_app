from datetime import datetime

from pydantic import model_validator

from src.application.contracts.base import Command, Result
from src.application.dtos import TickerDataDTO


class GetAllTickerDataFilteredCommand(Command):
    ticker_name: str
    min_date: datetime | None = None
    max_date: datetime | None = None

    @model_validator(mode="after")
    def validate(self):
        if self.min_date and self.max_date:
            if self.min_date >= self.max_date:
                raise ValueError("'min_date' must be less than 'max_date'")

        return self


class GetAllTickerDataFilteredResult(Result):
    result: list[TickerDataDTO]
