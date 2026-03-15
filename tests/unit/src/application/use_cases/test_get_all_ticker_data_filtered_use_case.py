from datetime import UTC, datetime, timedelta

import pytest

from src.application.contracts.get_all_ticker_data_filtered import (
    GetAllTickerDataFilteredCommand,
    GetAllTickerDataFilteredResult,
)
from src.application.dtos import TickerDataDTO
from src.application.use_cases import GetAllTickerDataFilteredUseCase
from src.application.use_cases.get_all_ticker_data_filtered import (
    FailedToGetAllTickerDataFiltered,
)


class TestGetAllTickerDataFilteredUseCase:
    @pytest.fixture
    def use_case(self, mock_transaction_manager_context, mock_logger):
        return GetAllTickerDataFilteredUseCase(
            logger=mock_logger,
            transaction_manager=mock_transaction_manager_context,
        )

    @pytest.mark.asyncio
    async def test_execute_successfully(
        self,
        use_case,
        mock_transaction_manager,
        sample_ticker_data_list,
    ):
        mock_transaction_manager.tickers_data.get_all_filtered_by_date.return_value = (
            sample_ticker_data_list
        )

        command = GetAllTickerDataFilteredCommand(
            ticker_name="btc_usd",
            min_date=datetime.now(tz=UTC) - timedelta(hours=1),
            max_date=datetime.now(tz=UTC),
        )

        result = await use_case(command)

        assert isinstance(result, GetAllTickerDataFilteredResult)
        assert len(result.result) == len(sample_ticker_data_list)
        assert isinstance(result.result[0], TickerDataDTO)
        assert result.result[0].timestamp == sample_ticker_data_list[0].timestamp

        mock_transaction_manager.tickers_data.get_all_filtered_by_date.assert_called_once_with(
            command.ticker_name, min_date=command.min_date, max_date=command.max_date
        )

    @pytest.mark.asyncio
    async def test_execute_empty_results(self, use_case, mock_transaction_manager):
        mock_transaction_manager.tickers_data.get_all_filtered_by_date.return_value = []

        command = GetAllTickerDataFilteredCommand(
            ticker_name="btc_usd",
            min_date=datetime.now(tz=UTC) - timedelta(hours=1),
            max_date=datetime.now(tz=UTC),
        )

        result = await use_case(command)

        assert isinstance(result, GetAllTickerDataFilteredResult)
        assert len(result.result) == 0

        mock_transaction_manager.tickers_data.get_all_filtered_by_date.assert_called_once_with(
            command.ticker_name, min_date=command.min_date, max_date=command.max_date
        )

    @pytest.mark.asyncio
    async def test_execute_transaction_manager_raises_exception(
        self, use_case, mock_transaction_manager
    ):
        mock_transaction_manager.tickers_data.get_all_filtered_by_date.side_effect = (
            Exception("test exception")
        )

        command = GetAllTickerDataFilteredCommand(
            ticker_name="btc_usd",
            min_date=datetime.now(tz=UTC) - timedelta(hours=1),
            max_date=datetime.now(tz=UTC),
        )

        with pytest.raises(FailedToGetAllTickerDataFiltered):
            await use_case(command)

        mock_transaction_manager.tickers_data.get_all_filtered_by_date.assert_called_once_with(
            command.ticker_name, min_date=command.min_date, max_date=command.max_date
        )
