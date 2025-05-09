from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# TODO: fix this test, it's taking too long to run
# def test_recommended_papers(user_id_token):
#     headers = {
#         "content-type": "application/json; charset=UTF-8",
#         "Authorization": f"Bearer {user_id_token}",
#     }
#     response = client.get("/recommended/", headers=headers, timeout=240)
#     assert response.status_code == 200
#     assert len(response.json()) > 0
