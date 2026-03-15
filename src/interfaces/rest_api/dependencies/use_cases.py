from typing import Annotated, TypeAlias

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.application.use_cases import (
    GetAllTickerDataFilteredUseCase,
    GetAllTickerDataUseCase,
    GetTickerLastRecordUseCase,
)
from src.infrastructure.di_config import ApplicationContainer


@inject
def get_get_all_ticker_data_use_case(
    get_all_ticker_data_use_case: GetAllTickerDataUseCase = Depends(
        Provide[ApplicationContainer.get_all_ticker_data_use_case]
    ),
) -> GetAllTickerDataUseCase:
    return get_all_ticker_data_use_case


@inject
def get_get_all_ticker_data_filtered_use_case(
    get_all_ticker_data_filtered_use_case: GetAllTickerDataFilteredUseCase = Depends(
        Provide[ApplicationContainer.get_all_ticker_data_filtered_use_case]
    ),
) -> GetAllTickerDataFilteredUseCase:
    return get_all_ticker_data_filtered_use_case


@inject
def get_get_ticker_data_last_record_use_case(
    get_ticker_data_last_record_use_case: GetTickerLastRecordUseCase = Depends(
        Provide[ApplicationContainer.get_ticker_data_last_record_use_case]
    ),
) -> GetTickerLastRecordUseCase:
    return get_ticker_data_last_record_use_case


GetAllTickerDataUseCaseDep: TypeAlias = Annotated[
    GetAllTickerDataUseCase,
    Depends(get_get_all_ticker_data_use_case),
]


GetAllTickerDataFilteredUseCaseDep: TypeAlias = Annotated[
    GetAllTickerDataFilteredUseCase,
    Depends(get_get_all_ticker_data_filtered_use_case),
]

GetTickerLastRecordUseCaseDep: TypeAlias = Annotated[
    GetTickerLastRecordUseCase,
    Depends(get_get_ticker_data_last_record_use_case),
]
