import pytest

from src.application.contracts.get_all_ticker_data import (
    GetAllTickerDataCommand,
    GetAllTickerDataResult,
)
from src.application.dtos import TickerDataDTO
from src.application.use_cases import GetAllTickerDataUseCase
from src.application.use_cases.get_all_ticker_data import FailedToGetAllTickerData


class TestGetAllTickerDataUseCase:
    @pytest.fixture
    def use_case(self, mock_transaction_manager_context, mock_logger):
        return GetAllTickerDataUseCase(
            logger=mock_logger,
            transaction_manager=mock_transaction_manager_context,
        )

    @pytest.mark.asyncio
    async def test_execute_successfully(
        self, use_case, mock_transaction_manager, sample_ticker_data_list
    ):
        mock_transaction_manager.tickers_data.get_all.return_value = (
            sample_ticker_data_list
        )

        command = GetAllTickerDataCommand(ticker_name="btc_usd")

        result = await use_case(command)

        assert isinstance(result, GetAllTickerDataResult)
        assert len(result.result) == len(sample_ticker_data_list)
        assert isinstance(result.result[0], TickerDataDTO)
        assert result.result[0].timestamp == sample_ticker_data_list[0].timestamp

        mock_transaction_manager.tickers_data.get_all.assert_called_once_with(
            command.ticker_name
        )

    @pytest.mark.asyncio
    async def test_execute_empty_results(self, use_case, mock_transaction_manager):
        mock_transaction_manager.tickers_data.get_all.return_value = []

        command = GetAllTickerDataCommand(ticker_name="btc_usd")

        result = await use_case(command)

        assert isinstance(result, GetAllTickerDataResult)
        assert len(result.result) == 0

        mock_transaction_manager.tickers_data.get_all.assert_called_once_with(
            command.ticker_name
        )

    @pytest.mark.asyncio
    async def test_execute_transaction_manager_raises_exception(
        self, use_case, mock_transaction_manager
    ):
        mock_transaction_manager.tickers_data.get_all.side_effect = Exception(
            "test exception"
        )

        command = GetAllTickerDataCommand(ticker_name="btc_usd")

        with pytest.raises(FailedToGetAllTickerData):
            await use_case(command)

        mock_transaction_manager.tickers_data.get_all.assert_called_once_with(
            command.ticker_name
        )
