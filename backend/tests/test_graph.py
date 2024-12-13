from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_graph(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    payload = {
        "doi": "10.1038/s41467-022-32094-6",
        "title": "Erasure conversion for fault-tolerant quantum computing in alkaline earth Rydberg atom arrays",
    }
    response = client.post("/graph/", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["citation_graph"] is not None
    assert response.json()["reference_graph"] is not None
