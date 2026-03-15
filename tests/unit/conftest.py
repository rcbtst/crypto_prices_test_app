from contextlib import nullcontext
from pathlib import Path
from unittest.mock import Mock

import pytest
from aioresponses import aioresponses
from pytest import Config, Item

from src.application.dtos import TickerDataDTO
from src.application.ports import ILogger, ITickerDataFetcher, ITransactionManager
from src.domain.entities import TickerData
from src.domain.repositories import ITickerDataRepository

UNIT_TESTS_DIR = Path(__file__).parent.resolve()


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    for item in items:
        if UNIT_TESTS_DIR in Path(item.fspath).resolve().parents:
            item.add_marker(pytest.mark.unit)


@pytest.fixture
def mock_logger():
    logger = Mock(spec=ILogger)
    logger.with_name.return_value = logger
    logger.with_context.return_value = logger
    logger.push_context.return_value = Mock()
    return logger


@pytest.fixture
def mock_transaction_manager():
    tm = Mock(spec=ITransactionManager)

    tm.tickers_data = Mock(spec=ITickerDataRepository)

    return tm


@pytest.fixture
def mock_transaction_manager_context(mock_transaction_manager):
    return nullcontext(mock_transaction_manager)


@pytest.fixture
def mock_ticker_data_fetcher():
    return Mock(spec=ITickerDataFetcher)


@pytest.fixture
def sample_ticker_data() -> TickerData:
    return TickerData(name="btc_usd", price=70234.51, timestamp=1773579083)


@pytest.fixture
def sample_ticker_data_list() -> list[TickerData]:
    return [
        TickerData(name="btc_usd", price=70234.51, timestamp=1773579083),
        TickerData(name="btc_usd", price=70232.1, timestamp=1773579023),
        TickerData(name="btc_usd", price=70231.0, timestamp=1773578985),
    ]


@pytest.fixture
def sample_ticker_data_dto(sample_ticker_data) -> TickerDataDTO:
    return TickerDataDTO(
        name=sample_ticker_data.name,
        price=sample_ticker_data.price,
        timestamp=sample_ticker_data.timestamp,
    )


@pytest.fixture
def sample_ticker_data_dto_list(sample_ticker_data_list) -> list[TickerDataDTO]:
    return [
        TickerDataDTO(
            name=ticker_data.name,
            price=ticker_data.price,
            timestamp=ticker_data.timestamp,
        )
        for ticker_data in sample_ticker_data_list
    ]


@pytest.fixture
def mock_aiohttp():
    with aioresponses() as m:
        yield m
