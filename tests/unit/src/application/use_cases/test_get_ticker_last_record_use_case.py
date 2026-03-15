import pytest

from src.application.contracts.get_ticker_last_record import (
    GetTickerLastRecordCommand,
    GetTickerLastRecordResult,
)
from src.application.dtos import TickerDataDTO
from src.application.use_cases import GetTickerLastRecordUseCase
from src.application.use_cases.get_ticker_last_record import FailedToGetLastTickerRecord


class TestGetTickerLastRecordUseCase:
    @pytest.fixture
    def use_case(self, mock_transaction_manager_context, mock_logger):
        return GetTickerLastRecordUseCase(
            logger=mock_logger,
            transaction_manager=mock_transaction_manager_context,
        )

    @pytest.mark.asyncio
    async def test_execute_successfully(
        self, use_case, mock_transaction_manager, sample_ticker_data
    ):
        mock_transaction_manager.tickers_data.get_last.return_value = sample_ticker_data

        command = GetTickerLastRecordCommand(ticker_name="btc_usd")

        result = await use_case(command)

        assert isinstance(result, GetTickerLastRecordResult)
        assert isinstance(result.result, TickerDataDTO)
        assert result.result.timestamp == sample_ticker_data.timestamp

        mock_transaction_manager.tickers_data.get_last.assert_called_once_with(
            command.ticker_name
        )

    @pytest.mark.asyncio
    async def test_execute_empty_result(self, use_case, mock_transaction_manager):
        mock_transaction_manager.tickers_data.get_last.return_value = None

        command = GetTickerLastRecordCommand(ticker_name="btc_usd")

        result = await use_case(command)

        assert isinstance(result, GetTickerLastRecordResult)
        assert result.result is None

        mock_transaction_manager.tickers_data.get_last.assert_called_once_with(
            command.ticker_name
        )

    @pytest.mark.asyncio
    async def test_execute_transaction_manager_raises_exception(
        self, use_case, mock_transaction_manager
    ):
        mock_transaction_manager.tickers_data.get_last.side_effect = Exception(
            "test exception"
        )

        command = GetTickerLastRecordCommand(ticker_name="btc_usd")

        with pytest.raises(FailedToGetLastTickerRecord):
            await use_case(command)

        mock_transaction_manager.tickers_data.get_last.assert_called_once_with(
            command.ticker_name
        )
