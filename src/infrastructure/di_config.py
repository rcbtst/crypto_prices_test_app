from dependency_injector import containers, providers

from src.application.use_cases import (
    GetAllTickerDataFilteredUseCase,
    GetAllTickerDataUseCase,
    GetTickerLastRecordUseCase,
    UpdateTickerDataUseCase,
)
from src.config import settings
from src.infrastructure.database import SQLAlchemyDatabase, SQLAlchemyTransactionManager
from src.infrastructure.external_apis import DeribitAPIClient, DeribitTickerDataFetcher
from src.infrastructure.utils import StdLibLogger


class ApplicationContainer(containers.DeclarativeContainer):
    logger = providers.Factory(StdLibLogger)

    db = providers.Singleton(
        SQLAlchemyDatabase,
        url=settings.build_db_url(),
        logger=logger,
        echo=False,
        pool_pre_ping=True,
    )

    transaction_manager = providers.Factory(
        SQLAlchemyTransactionManager,
        session_factory=db.provided.session_factory,
        logger=logger,
    )

    deribit_api_client = providers.Factory(
        DeribitAPIClient,
        logger=logger,
    )

    ticker_data_fetcher = providers.Factory(
        DeribitTickerDataFetcher,
        deribit_api_client=deribit_api_client,
        logger=logger,
    )

    update_ticker_data_use_case = providers.Factory(
        UpdateTickerDataUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
        ticker_data_fetcher=ticker_data_fetcher,
    )

    get_all_ticker_data_use_case = providers.Factory(
        GetAllTickerDataUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    get_all_ticker_data_filtered_use_case = providers.Factory(
        GetAllTickerDataFilteredUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )

    get_ticker_data_last_record_use_case = providers.Factory(
        GetTickerLastRecordUseCase,
        logger=logger,
        transaction_manager=transaction_manager,
    )
