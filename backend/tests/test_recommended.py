from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_recommended_papers(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    response = client.get("/recommended/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
