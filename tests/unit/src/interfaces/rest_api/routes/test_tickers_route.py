from unittest.mock import AsyncMock

import pytest

from src.application.contracts.get_all_ticker_data import GetAllTickerDataResult
from src.application.contracts.get_all_ticker_data_filtered import (
    GetAllTickerDataFilteredResult,
)
from src.application.contracts.get_ticker_last_record import GetTickerLastRecordResult
from src.application.use_cases import (
    GetAllTickerDataFilteredUseCase,
    GetAllTickerDataUseCase,
    GetTickerLastRecordUseCase,
)


class TestTickersRoute:
    @pytest.mark.asyncio
    async def test_get_all_ticker_data(
        self, test_rest_api_client, sample_ticker_data_dto_list, fastapi_app
    ):
        use_case_mock = AsyncMock(spec=GetAllTickerDataUseCase)
        use_case_mock.return_value = GetAllTickerDataResult(
            result=sample_ticker_data_dto_list
        )

        with fastapi_app.container.get_all_ticker_data_use_case.override(use_case_mock):
            response = await test_rest_api_client.get(
                "/tickers/get_all", params={"ticker_name": "btc_usd"}
            )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert len(data["result"]) == len(sample_ticker_data_dto_list)

    @pytest.mark.asyncio
    async def test_get_all_filtered_ticker_data(
        self, test_rest_api_client, sample_ticker_data_dto_list, fastapi_app
    ):
        use_case_mock = AsyncMock(spec=GetAllTickerDataFilteredUseCase)
        use_case_mock.return_value = GetAllTickerDataFilteredResult(
            result=sample_ticker_data_dto_list
        )

        with fastapi_app.container.get_all_ticker_data_filtered_use_case.override(
            use_case_mock
        ):
            response = await test_rest_api_client.get(
                "/tickers/get_all_filtered",
                params={
                    "ticker_name": "btc_usd",
                    "min_date": "2026-03-15T16:43:07.028Z",
                    "max_date": "2026-03-15T16:53:07.028Z",
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert len(data["result"]) == len(sample_ticker_data_dto_list)

    @pytest.mark.asyncio
    async def test_get_last_ticker_data(
        self, test_rest_api_client, sample_ticker_data_dto, fastapi_app
    ):
        use_case_mock = AsyncMock(spec=GetTickerLastRecordUseCase)
        use_case_mock.return_value = GetTickerLastRecordResult(
            result=sample_ticker_data_dto
        )

        with fastapi_app.container.get_ticker_data_last_record_use_case.override(
            use_case_mock
        ):
            response = await test_rest_api_client.get(
                "/tickers/get_last", params={"ticker_name": "btc_usd"}
            )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert data["result"]["price"] == sample_ticker_data_dto.price
