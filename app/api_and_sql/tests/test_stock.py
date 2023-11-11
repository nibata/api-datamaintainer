from httpx import AsyncClient
from ..main import app
import pytest


@pytest.fixture
def anyio_backend(db):
    return 'asyncio'


@pytest.mark.anyio
async def test_get_movement_product():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/stock?product=product 1")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_movement_all_product():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/stock/all")

    assert response.status_code == 200
