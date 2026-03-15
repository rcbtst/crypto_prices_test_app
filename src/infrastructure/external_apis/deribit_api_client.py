from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Type

from aiohttp import ClientSession
from pydantic import BaseModel, ConfigDict
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from src.application.ports import ILogger


class TickerIndexPriceResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    index_price: float


class NoOpenSessionException(Exception):
    pass


class IDeribitAPIClient(ABC):
    @abstractmethod
    async def __aenter__(self) -> "IDeribitAPIClient":
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ):
        pass

    @abstractmethod
    async def get_ticker_index_price(
        self, ticker_name: str
    ) -> TickerIndexPriceResponse:
        pass


class DeribitAPIClient(IDeribitAPIClient):
    def __init__(
        self,
        logger: ILogger,
        base_url: str = "https://www.deribit.com/api/v2/",
        custom_session: ClientSession | None = None,
    ):
        self._logger = logger.with_name(__name__)
        self._base_url = base_url if base_url.endswith("/") else f"{base_url}/"
        self._session = custom_session
        self._own_session_used = custom_session is None

    def _create_own_session(self) -> ClientSession:
        return ClientSession(base_url=self._base_url)

    async def __aenter__(self) -> "DeribitAPIClient":
        if self._session is None or self._session.closed:
            self._logger.debug("Creating new http session")
            self._session = self._create_own_session()
            self._own_session_used = True

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ):
        if self._session and self._own_session_used:
            self._logger.debug("Closing http session")
            await self._session.close()

    def _ensure_session_exists(self):
        if self._session is None or self._session.closed:
            self._logger.error("API call without open session attempt")
            raise NoOpenSessionException(
                "No open http session found. Use context manager or provide custom session first"
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(multiplier=1, max=10),
        retry=retry_if_not_exception_type(NoOpenSessionException),
        reraise=True,
    )
    async def _make_api_request(
        self, method: str, path: str, query_params: dict | None = None
    ):
        self._ensure_session_exists()

        try:
            async with self._session.request(
                method.upper(), path.lstrip("/"), params=query_params
            ) as response:
                response.raise_for_status()
                response_json = await response.json()

            result = response_json["result"]

            return result
        except Exception:
            self._logger.exception("API call failed")
            raise

    async def get_ticker_index_price(
        self, ticker_name: str
    ) -> TickerIndexPriceResponse:
        result = await self._make_api_request(
            "GET", "public/get_index_price", query_params={"index_name": ticker_name}
        )

        return TickerIndexPriceResponse(**result)
