from ..configs.settings import PASS_ADMIN, ADMIN_EMAIL
from httpx import AsyncClient
from ..main import app
import pytest


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
        "fullname": "No Authorized User",
        "email": "no@authorized.com",
        "password": "pwd_test"
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/users", json=json)

    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_user_in_id_1():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q?user_id=1")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_user():
    json_token = {
        "Email": ADMIN_EMAIL,
        "Password": PASS_ADMIN
    }

    print("#" * 10)
    print("#" * 10)
    print("#" * 10)
    print(ADMIN_EMAIL, PASS_ADMIN)
    print("#" * 10)
    print("#" * 10)
    print("#" * 10)

    json_insert = {
        "FullName": "User Test Two",
        "Email": "user@test.com",
        "Password": "pwd_test",
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_test = await async_client.post("/users", json=json_insert, headers=headers)

    assert response_test.status_code == 200
