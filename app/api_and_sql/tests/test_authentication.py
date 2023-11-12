from ..configs.settings import PASS_ADMIN, ADMIN_EMAIL
from httpx import AsyncClient
from ..main import app
import pytest


@pytest.fixture
def anyio_backend(db):
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
    json_wrong_pwd_token = {
        "email": ADMIN_EMAIL,
        "password": "WRONG_PWD"
    }

    json_not_existing_mail_token = {
        "email": "not@existing.com",
        "password": "WRONG_PWD"
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_wrong_pwd_token = await async_client.post("/user/login", json=json_wrong_pwd_token)
        response_not_existing_mail_token = await async_client.post("/user/login", json=json_not_existing_mail_token)

    assert response_wrong_pwd_token.status_code == 200
    assert response_wrong_pwd_token.json()["error"] == "Wrong login details"

    assert response_not_existing_mail_token.status_code == 200


@pytest.mark.anyio
async def test_create_use_and_create_update_password():
    json_token = {
        "email": ADMIN_EMAIL,
        "password": PASS_ADMIN
    }

    json_insert = {
        "full-name": "User Test Two",
        "email": "user@test.com",
        "password": "pwd_test",
    }

    json_update = {
        "email": "user@test.com",
        "current-password": "pwd_test",
        "new-password": "pwd_test_updated",
        "expiration-date": "2099-11-11"
    }

    json_update_email_does_not_exist = {
        "email": "userr@test.com",
        "current-password": "pwd_test",
        "new-password": "pwd_test_updated",
        "expiration-date": "2099-11-11"
    }

    json_create_password = {
        "email": "user@test.com",
        "password": "pwd_test",
        "expiration-date": "2099-11-12"
    }

    json_create_password_not_existing_mail = {
        "email": "userr@test.com",
        "password": "pwd_test",
        "expiration-date": "2099-11-12"
    }

    json_deactivate_password = {
        "email": "user@test.com",
    }

    json_deactivate_password_not_exist_email = {
        "email": "userr@test.com",
    }
    async with (AsyncClient(app=app, base_url="http://test") as async_client):
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_insert_test = await async_client.post("/users",
                                                       json=json_insert,
                                                       headers=headers)

        response_update_test = await async_client.post("/password/update_password",
                                                       json=json_update,
                                                       headers=headers)

        # debido a que en el punto anterior se actualizó la pass usar el mismo body debería resultar en un error
        response_update_wrong_password_test = await async_client.post("/password/update_password",
                                                                      json=json_update,
                                                                      headers=headers)

        response_update_email_does_not_exist_test = await async_client.post("/password/update_password",
                                                                            json=json_update_email_does_not_exist,
                                                                            headers=headers)

        response_create_password_already_active = await async_client.post("/password/create_password",
                                                                          json=json_create_password,
                                                                          headers=headers)

        response_deactivate_password = await async_client.post("/password/deactivate_password",
                                                               json=json_deactivate_password,
                                                               headers=headers)

        response_deactivate_password_not_exist_email = await async_client.post(
            "/password/deactivate_password",
            json=json_deactivate_password_not_exist_email,
            headers=headers)

        response_update_password_to_deactivates_one = await async_client.post("/password/update_password",
                                                                              json=json_update,
                                                                              headers=headers)

        response_create_password_to_deactivated_one = await async_client.post("/password/create_password",
                                                                              json=json_create_password,
                                                                              headers=headers)

        response_create_password_not_existing_email = await async_client.post(
            "/password/create_password",
            json=json_create_password_not_existing_mail,
            headers=headers)

    assert response_insert_test.status_code == 200
    assert response_update_test.status_code == 200
    assert response_update_wrong_password_test.status_code == 400
    assert response_update_email_does_not_exist_test.status_code == 400
    assert response_create_password_already_active.status_code == 400
    assert response_deactivate_password.status_code == 200
    assert response_deactivate_password_not_exist_email.status_code == 400
    assert response_update_password_to_deactivates_one.status_code == 400
    assert response_create_password_to_deactivated_one.status_code == 200
    assert response_create_password_not_existing_email.status_code == 400


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


@pytest.mark.anyio
async def test_create_group():
    json_token = {
        "email": ADMIN_EMAIL,
        "password": PASS_ADMIN
    }

    json_insert = {
        "code": "TEST",
        "description": "Descripción"
    }

    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_token = await async_client.post("/user/login", json=json_token)
        auth_token = response_token.json()["access_token"]

        headers = {"Authorization": f"Bearer {auth_token}"}
        response_first_insert_test = await async_client.post("/groups", json=json_insert, headers=headers)
        response_second_insert_test = await async_client.post("/groups", json=json_insert, headers=headers)

    assert response_first_insert_test.status_code == 200
    assert response_second_insert_test.status_code == 400


@pytest.mark.anyio
async def test_get_group():
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response_get_group_test = await async_client.get("/groups")

    assert response_get_group_test.status_code == 200
