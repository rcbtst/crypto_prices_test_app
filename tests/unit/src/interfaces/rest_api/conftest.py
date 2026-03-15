from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.interfaces.rest_api import WebApiApp, setup_app


@pytest.fixture(scope="session")
def fastapi_app() -> Generator[WebApiApp, None, None]:
    app = setup_app()
    yield app


@pytest_asyncio.fixture
async def test_rest_api_client(
    fastapi_app: WebApiApp,
) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test/"
    ) as client:
        yield client
