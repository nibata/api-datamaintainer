import pytest
from ..main import app
from httpx import AsyncClient
from ..configs.settings import USER_ADMIN, PASS_ADMIN


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_check_life_of_users_route():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users")
    
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_user_without_authorization():
    json = {
        "fullname": "Nicolás Bacquet",
        "email": "nibata@gmail.com",
        "password": "pwd_test"
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/users", json=json)

    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_user_nibata_in_id_1():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q?user_id=1")

    assert response.json() == {
        "fullname": "Nicolás Bacquet",
        "email": "nibata@gmail.com", 
        "id": 1, 
        "is_active": True
    }


@pytest.mark.anyio
async def test_create_user():
    json_token = {
        "email": USER_ADMIN,
        "password": PASS_ADMIN
    }

    json_insert = {
        "fullname": "test",
        "email": "test@test.test",
        "password": "pwd_test",
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_test = await async_client.post("/users", json=json_insert, headers=headers)

    assert response_test.status_code == 200
