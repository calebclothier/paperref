from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_service_success():
    payload = {"email": "testuser@gmail.com", "password": "test123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert "id_token" in response.json()
    assert "refresh_token" in response.json()
    assert "expires_in" in response.json()
    

def test_login_service_invalid_email():
    payload = {"email": "testuser@gmail", "password": "test123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials."
    

def test_login_service_invalid_password():
    payload = {"email": "testuser@gmail.com", "password": "test"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials."


def test_login_service_missing_password():
    payload = {"email": "testuser@gmail.com", "password": ""}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing password."


def test_register_service_email_exists():
    payload = {"email": "testuser@gmail.com", "password": "test123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Account already exists for provided email address."


def test_register_service_weak_password():
    payload = {"email": "newuser@gmail.com", "password": "test"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Weak password, must contain at least 6 characters."
    
    
def test_register_service_invalid_email():
    payload = {"email": "newuser@gmail", "password": "test123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email."


def test_refresh_id_token_service_success(user_refresh_token):
    response = client.post(f"/auth/refresh_token?refresh_token={user_refresh_token}")
    assert response.status_code == 200
    assert 'id_token' in response.json()
    assert 'expires_in' in response.json()


def test_refresh_id_token_service_invalid_token():
    user_refresh_token = "invalid_refresh_token"
    response = client.post(f"/auth/refresh_token?refresh_token={user_refresh_token}")
    assert response.status_code != 200
