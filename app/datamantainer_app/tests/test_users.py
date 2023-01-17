from ..main import app
from fastapi.testclient import TestClient


client = TestClient(app=app)


def test_check_life_of_users_route():
    response = client.get("/users")
    
    assert response.status_code == 200


def test_create_user():
    json = {
        "email": "nibata@gmail.com",
        "password": "pwd_test"
    }

    response = client.post("/users", json=json)

    assert response.status_code == 200


def test_get_user_nibata_in_id_1():
    response = client.get("/users?user_id=1")

    assert response.json() == [{
        "email": "nibata@gmail.com", 
        "id": 1, 
        "is_active": False
    }]
