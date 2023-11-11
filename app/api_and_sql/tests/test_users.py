from ..configs.settings import PASS_ADMIN, ADMIN_EMAIL
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
        response = await async_client.get("/users/q?user-id=1")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_not_found():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q?user-id=0")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_user_by_email():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q?user-email=nibata@gmail.com")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_not_found_by_email():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q?user-email=not@existing.com")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_user_not_given_user():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/users/q")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_loging_wrong_credential():
    json_token = {
        "email": ADMIN_EMAIL,
        "password": "WRONG_PWD"
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)

    assert response_token.status_code == 200
    assert response_token.json()["error"] == "Wrong login details"


@pytest.mark.anyio
async def test_create_user():
    json_token = {
        "email": ADMIN_EMAIL,
        "password": PASS_ADMIN
    }

    json_insert = {
        "full-name": "User Test Two",
        "email": "user@test.com",
        "password": "pwd_test",
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_test = await async_client.post("/users", json=json_insert, headers=headers)

    assert response_test.status_code == 200


@pytest.mark.anyio
async def test_create_user_already_registered():
    json_token = {
        "email": ADMIN_EMAIL,
        "password": PASS_ADMIN
    }

    json_insert = {
        "full-name": "User Test Two",
        "email": ADMIN_EMAIL,
        "password": "pwd_test",
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_test = await async_client.post("/users", json=json_insert, headers=headers)

    assert response_test.status_code == 400


@pytest.mark.anyio
async def test_create_user_not_valid_token():
    json_insert = {
        "full-name": "User Test Two",
        "email": "user@test.com",
        "password": "pwd_test",
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        auth_invalid_token = "INVALID TOKEN"
        auth_autogen_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjoiZ0FBQUFBQmxUM0NXdl9vZzFBOWxkTHVRWDZFQ3l"
                              "4TG03R2lEWXZqMmhyWHZ3TUlzRjNhVDFpbGxkYk9UdUUycXRVRmxGN2lReUZxdWtmR2VWWHBoa2g3bGVlMjA1Zz"
                              "ZaUml3UnR6LV8yUk9mTWxwd0hWYm8yTkFOVXhSamt2SUNiRzVRR1VZWWwwWlVEaFd0NUM1dThzUGNUV3BkMTJ0WD"
                              "JWRUhUekFwdG1XODdOZTRwVWNCcGFfcm93NHFTZmNnSzVQVElWOG5EdWlaT0FKUmdRUlpJMlVpTG5lbmlfQ284UE"
                              "tENlVaM3ltYUFzUFdTLWp6RHBLST0ifQ.0Wj4zK5x47AR5XnIwmQ8UsekFqVB6-OO3wGn5vtodSs")

        headers_invalid_token = {"Authorization": f"Bearer {auth_invalid_token}"}
        headers_autogen_token = {"Authorization": f"Bearer {auth_autogen_token}"}

        response_headers_invalid_token_test = await async_client.post("/users",
                                                                      json=json_insert,
                                                                      headers=headers_invalid_token)

        response_autogen_token = await async_client.post("/users",
                                                         json=json_insert,
                                                         headers=headers_autogen_token)

    assert response_headers_invalid_token_test.status_code == 403
    assert response_autogen_token.status_code == 403
