from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from src.application.dtos import TickerDataDTO


class TickerDataRequestParams(BaseModel):
    ticker_name: str


class FilteredTickerDataRequestParams(TickerDataRequestParams):
    min_date: datetime | None = None
    max_date: datetime | None = None

    @model_validator(mode="after")
    def validate(self):
        if self.min_date and self.max_date:
            if self.min_date >= self.max_date:
                raise ValueError("'min_date' must be less than 'max_date'")

        return self


class TickerDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    result: TickerDataDTO | list[TickerDataDTO] | None = None
