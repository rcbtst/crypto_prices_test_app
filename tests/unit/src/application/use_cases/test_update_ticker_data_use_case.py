import pytest

from src.application.contracts.base import NoneResult
from src.application.contracts.update_ticker_data import UpdateTickerDataCommand
from src.application.use_cases import UpdateTickerDataUseCase
from src.application.use_cases.update_ticker_data import FailedToUpdateTickerData
from src.domain.entities import TickerData


class TestUpdateTickerDataUseCase:
    @pytest.fixture
    def use_case(
        self, mock_transaction_manager_context, mock_logger, mock_ticker_data_fetcher
    ):
        return UpdateTickerDataUseCase(
            logger=mock_logger,
            transaction_manager=mock_transaction_manager_context,
            ticker_data_fetcher=mock_ticker_data_fetcher,
        )

    @pytest.mark.asyncio
    async def test_execute_successfully(
        self,
        use_case,
        mock_transaction_manager,
        mock_ticker_data_fetcher,
        sample_ticker_data_dto,
    ):
        mock_ticker_data_fetcher.fetch_new_ticker_data.return_value = (
            sample_ticker_data_dto
        )

        command = UpdateTickerDataCommand(ticker_name="btc_usd")

        result = await use_case(command)

        assert isinstance(result, NoneResult)

        mock_ticker_data_fetcher.fetch_new_ticker_data.assert_called_once_with(
            command.ticker_name
        )
        mock_transaction_manager.tickers_data.save.assert_called_once()
        saved_ticker_data = mock_transaction_manager.tickers_data.save.call_args[0][0]

        assert isinstance(saved_ticker_data, TickerData)
        assert saved_ticker_data.price == sample_ticker_data_dto.price
        assert saved_ticker_data.timestamp == sample_ticker_data_dto.timestamp
        assert saved_ticker_data.name == sample_ticker_data_dto.name

    @pytest.mark.asyncio
    async def test_execute_ticker_data_fetcher_raises_exception(
        self, use_case, mock_transaction_manager, mock_ticker_data_fetcher
    ):
        mock_ticker_data_fetcher.fetch_new_ticker_data.side_effect = Exception(
            "test exception"
        )

        command = UpdateTickerDataCommand(ticker_name="btc_usd")

        with pytest.raises(FailedToUpdateTickerData):
            await use_case(command)

        mock_ticker_data_fetcher.fetch_new_ticker_data.assert_called_once_with(
            command.ticker_name
        )
        mock_transaction_manager.tickers_data.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_transaction_manager_raises_exception(
        self,
        use_case,
        mock_transaction_manager,
        mock_ticker_data_fetcher,
        sample_ticker_data_dto,
    ):
        mock_ticker_data_fetcher.fetch_new_ticker_data.return_value = (
            sample_ticker_data_dto
        )
        mock_transaction_manager.tickers_data.save.side_effect = Exception(
            "test exception"
        )

        command = UpdateTickerDataCommand(ticker_name="btc_usd")

        with pytest.raises(FailedToUpdateTickerData):
            await use_case(command)

        mock_ticker_data_fetcher.fetch_new_ticker_data.assert_called_once_with(
            command.ticker_name
        )
        mock_transaction_manager.tickers_data.save.assert_called_once()
        saved_ticker_data = mock_transaction_manager.tickers_data.save.call_args[0][0]

        assert isinstance(saved_ticker_data, TickerData)
        assert saved_ticker_data.price == sample_ticker_data_dto.price
        assert saved_ticker_data.timestamp == sample_ticker_data_dto.timestamp
        assert saved_ticker_data.name == sample_ticker_data_dto.name
