from httpx import AsyncClient
from ..main import app
import pytest


try:
    @pytest.fixture
    def anyio_backend(db):
        return 'asyncio'
except ValueError as er:
    @pytest.fixture
    def anyio_backend():
        return 'asyncio'


@pytest.mark.anyio
async def test_default_page():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/")
        response_content = response.json()

    assert response.status_code == 200
    assert response_content["app"] == "API AND SQL"


@pytest.mark.anyio
async def test_sentry():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        try:
            response = await async_client.get("/test_sentry")
        except ZeroDivisionError as er:
            response = str(er)

    assert response == "division by zero"

