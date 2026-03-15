from typing import Annotated

from fastapi import APIRouter, Query

from src.application.contracts.get_all_ticker_data import (
    GetAllTickerDataCommand,
    GetAllTickerDataResult,
)
from src.application.contracts.get_all_ticker_data_filtered import (
    GetAllTickerDataFilteredCommand,
    GetAllTickerDataFilteredResult,
)
from src.application.contracts.get_ticker_last_record import (
    GetTickerLastRecordCommand,
    GetTickerLastRecordResult,
)
from src.interfaces.rest_api.dependencies import (
    GetAllTickerDataFilteredUseCaseDep,
    GetAllTickerDataUseCaseDep,
    GetTickerLastRecordUseCaseDep,
)
from src.interfaces.rest_api.models import (
    FilteredTickerDataRequestParams,
    TickerDataRequestParams,
    TickerDataResponse,
)

router = APIRouter(prefix="/tickers", tags=["tickers"])


@router.get("/get_all")
async def get_all_ticker_data(
    query: Annotated[TickerDataRequestParams, Query()],
    get_all_ticker_data_use_case: GetAllTickerDataUseCaseDep,
) -> TickerDataResponse:
    result: GetAllTickerDataResult = await get_all_ticker_data_use_case(
        GetAllTickerDataCommand(ticker_name=query.ticker_name)
    )

    return TickerDataResponse.model_validate(result)


@router.get("/get_all_filtered")
async def get_all_filtered_ticker_data(
    query: Annotated[FilteredTickerDataRequestParams, Query()],
    get_all_ticker_data_filtered_use_case: GetAllTickerDataFilteredUseCaseDep,
) -> TickerDataResponse:
    result: GetAllTickerDataFilteredResult = (
        await get_all_ticker_data_filtered_use_case(
            GetAllTickerDataFilteredCommand(
                ticker_name=query.ticker_name,
                min_date=query.min_date,
                max_date=query.max_date,
            )
        )
    )

    return TickerDataResponse.model_validate(result)


@router.get("/get_last")
async def get_last_ticker_data(
    query: Annotated[TickerDataRequestParams, Query()],
    get_ticker_data_last_record_use_case: GetTickerLastRecordUseCaseDep,
) -> TickerDataResponse:
    result: GetTickerLastRecordResult = await get_ticker_data_last_record_use_case(
        GetTickerLastRecordCommand(ticker_name=query.ticker_name)
    )

    return TickerDataResponse.model_validate(result)
