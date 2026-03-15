import pytest

from src.infrastructure.external_apis.deribit_api_client import (
    DeribitAPIClient,
    NoOpenSessionException,
    TickerIndexPriceResponse,
)


class TestDeribitAPIClient:
    @pytest.mark.asyncio
    async def test_get_ticker_index_price_success_request(
        self, mock_logger, mock_aiohttp
    ):
        test_price = 71234.567
        url = "https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd"

        mock_aiohttp.get(
            url,
            payload={"result": {"index_price": test_price, "extra_data": "test"}},
        )

        async with DeribitAPIClient(logger=mock_logger) as client:
            response = await client.get_ticker_index_price("btc_usd")

        assert isinstance(response, TickerIndexPriceResponse)
        assert response.index_price == test_price

        mock_aiohttp.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_ticker_index_price_retries_on_failures(
        self, mock_logger, mock_aiohttp
    ):
        test_price = 71234.567
        url = "https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd"

        mock_aiohttp.get(url, status=500)
        mock_aiohttp.get(
            url,
            payload={"result": {"index_price": test_price, "extra_data": "test"}},
        )

        async with DeribitAPIClient(logger=mock_logger) as client:
            response = await client.get_ticker_index_price("btc_usd")

        assert isinstance(response, TickerIndexPriceResponse)
        assert response.index_price == test_price

        mock_aiohttp.assert_called()

    @pytest.mark.asyncio
    async def test_client_usage_not_allowed_without_session(self, mock_logger):
        with pytest.raises(NoOpenSessionException):
            await DeribitAPIClient(logger=mock_logger).get_ticker_index_price("btc_usd")
