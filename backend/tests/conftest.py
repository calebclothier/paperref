import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="session")
def user_id_token():
    """Fixture to login a user and return their id_token."""
    payload = {"email": "testuser@gmail.com", "password": "test123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    return response.json()["id_token"]


@pytest.fixture(scope="session")
def user_refresh_token():
    """Fixture to login a user and return their id_token."""
    payload = {"email": "testuser@gmail.com", "password": "test123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    return response.json()["refresh_token"]
