from celery import shared_task
from dependency_injector.wiring import Provide, inject

from src.application.contracts.update_ticker_data import UpdateTickerDataCommand
from src.application.use_cases import UpdateTickerDataUseCase
from src.infrastructure.di_config import ApplicationContainer
from src.interfaces.workers.tasks.base import AsyncTask


@shared_task(name="update_tickers_data", base=AsyncTask)
@inject
async def update_tickers_data_task(
    tickers_to_update: tuple[str],
    update_ticker_data_use_case: UpdateTickerDataUseCase = Provide[
        ApplicationContainer.update_ticker_data_use_case
    ],
):
    for ticker_name in tickers_to_update:
        await update_ticker_data_use_case(
            UpdateTickerDataCommand(ticker_name=ticker_name)
        )
