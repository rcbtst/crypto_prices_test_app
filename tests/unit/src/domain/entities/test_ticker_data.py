import pytest
from pydantic import ValidationError

from src.domain.entities.ticker_data import TickerData


class TestTickerDataEntity:
    def test_create_with_valid_args(self):
        new_ticker_data = TickerData(name="btc_usd", price=500.5, timestamp=1773579083)

        assert new_ticker_data.id is not None
        assert new_ticker_data.name == "btc_usd"
        assert new_ticker_data.price == 500.5
        assert new_ticker_data.timestamp == 1773579083

    def test_create_with_int_price(self):
        new_ticker_data = TickerData(name="btc_usd", price=500, timestamp=1773579083)

        assert new_ticker_data.id is not None
        assert new_ticker_data.name == "btc_usd"
        assert new_ticker_data.price == 500
        assert new_ticker_data.timestamp == 1773579083

    def test_create_without_name(self):
        with pytest.raises(ValidationError):
            TickerData(price=500.5, timestamp=1773579083)

    def test_create_without_price(self):
        with pytest.raises(ValidationError):
            TickerData(name="btc_usd", timestamp=1773579083)

    def test_create_without_timestamp(self):
        with pytest.raises(ValidationError):
            TickerData(name="btc_usd", price=500.5)

    def test_create_with_empty_name(self):
        with pytest.raises(ValidationError):
            TickerData(name="", price=500.5, timestamp=1773579083)

    def test_create_with_invalid_price(self):
        with pytest.raises(ValidationError):
            TickerData(name="btc_usd", price="abc", timestamp=1773579083)

    def test_create_with_invalid_timestamp(self):
        with pytest.raises(ValidationError):
            TickerData(name="btc_usd", price=500.5, timestamp="2026-03-15 10:30:03")
