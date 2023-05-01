from ..main import app
from fastapi.testclient import TestClient
from ..configs.settings import USER_ADMIN, PASS_ADMIN

client = TestClient(app=app)


def test_check_life_of_users_route():
    response = client.get("/users")
    
    assert response.status_code == 200


def test_create_user_without_authorization():
    json = {
        "fullname": "Nicolás Bacquet",
        "email": "nibata@gmail.com",
        "password": "pwd_test"
    }

    response = client.post("/users", json=json)

    assert response.status_code == 403


def test_get_user_nibata_in_id_1():
    response = client.get("/users/q?user_id=1")
    assert response.json() == {
        "fullname": "Nicolás Bacquet",
        "email": "nibata@gmail.com", 
        "id": 1, 
        "is_active": True
    }

def test_create_user():
    json_token = {
        "email": USER_ADMIN,
        "password": PASS_ADMIN
    }

    json_insert = {
         "fullname": "test",
         "email": "test@test.test", 
         "password": "pwd_test",
    }

    response_token = client.post("/user/login", json=json_token)
    auth_token = response_token.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    response_test = client.post("/users", json=json_insert, headers=headers)

    assert response_test.status_code == 200

