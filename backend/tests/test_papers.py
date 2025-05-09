from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_paper(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    payload = {
        'id': '43f52802fc640cb74e9c742fb6f1d272cd17cec6', 
         'title': 'High-fidelity gates and mid-circuit erasure conversion in an atomic qubit', 
         'doi': '10.1038/s41586-023-06438-1', 
         'arxiv': None, 
         'authors': [
             'Shuo Ma', 'Genyue Liu', 'Pai Peng', 'Bichen Zhang',
             'Sven Jandura', 'J. Claes', 'Alex P. Burgers', 'G. Pupillo', 
             'S. Puri', 'Jeff D. Thompson'], 
         'abstract': None, 
         'year': 2023, 
         'publication_date': '2023-10-01', 
         'reference_count': 58, 
         'citation_count': 133, 
         'journal': 'Nature', 
         'open_access_url': '', 
         'tldr': None}
    response = client.post("/library/papers/add", headers=headers, json=payload)
    assert response.status_code == 200


def test_load_papers(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    response = client.get("/library/papers", headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {'id': '43f52802fc640cb74e9c742fb6f1d272cd17cec6', 
         'title': 'High-fidelity gates and mid-circuit erasure conversion in an atomic qubit', 
         'doi': '10.1038/s41586-023-06438-1', 
         'arxiv': None, 
         'authors': [
             'Shuo Ma', 'Genyue Liu', 'Pai Peng', 'Bichen Zhang',
             'Sven Jandura', 'J. Claes', 'Alex P. Burgers', 'G. Pupillo', 
             'S. Puri', 'Jeff D. Thompson'], 
         'abstract': None, 
         'year': 2023, 
         'publication_date': '2023-10-01', 
         'reference_count': 58, 
         'citation_count': 133, 
         'journal': 'Nature', 
         'open_access_url': '', 
         'tldr': None}
    ]


def test_delete_paper(user_id_token):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {user_id_token}",
    }
    paper_id = "43f52802fc640cb74e9c742fb6f1d272cd17cec6"
    response = client.delete(f"/library/papers/{paper_id}", headers=headers)
    assert response.status_code == 200
