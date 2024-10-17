import base64

from app.database.firestore import db
from app.schemas.library import Paper



def generate_firestore_id_from_doi(doi):
    return base64.urlsafe_b64encode(doi.encode('utf-8')).decode('utf-8').rstrip('=')
    
    
def get_paper_library_service(user_id: str):
    papers_ref = db.collection("users").document(user_id).collection("papers")
    papers = papers_ref.stream()
    paper_list = []
    for paper in papers:
        paper_dict = paper.to_dict()
        paper_list.append(Paper(**paper_dict))
    return paper_list


def save_paper_library_service(user_id: str, paper_data: list[Paper]):
    papers_ref = db.collection("users").document(user_id).collection("papers")
    saved_papers = papers_ref.stream()
    ids_to_keep = [generate_firestore_id_from_doi(paper.doi) for paper in paper_data]
    for paper in saved_papers:
        if paper.id not in ids_to_keep:
            papers_ref.document(paper.id).delete()
    for paper in paper_data:
        paper_id = generate_firestore_id_from_doi(paper.doi)
        papers_ref.document(paper_id).set(paper.model_dump())