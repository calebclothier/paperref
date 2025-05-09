from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_load_papers(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    response = client.get("/library/papers", headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "1234567890",
            "title": "Erasure conversion for fault-tolerant quantum computing in alkaline earth Rydberg atom arrays",
            "doi": "10.1038/s41467-022-32094-6",
            "authors": ["Author 1", "Author 2"],
            "year": 2022,
            "journal": "Nature Communications",
            "abstract": "Abstract text here",
            "citation_count": 42,
            "reference_count": 50,
        }
    ]


def test_save_papers(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    payload = [
        {
            "id": "1234567890",
            "title": "Erasure conversion for fault-tolerant quantum computing in alkaline earth Rydberg atom arrays",
            "doi": "10.1038/s41467-022-32094-6",
            "authors": ["Author 1", "Author 2"],
            "year": 2022,
            "journal": "Nature Communications",
            "abstract": "Abstract text here",
            "citation_count": 42,
            "reference_count": 50,
        }
    ]
    response = client.post("/library/papers", headers=headers, json=payload)
    assert response.status_code == 200
