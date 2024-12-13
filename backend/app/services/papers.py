"""Paper services for managing a user's paper library in Firestore."""

import base64

from app.database.firestore import db
from app.schemas.papers import Paper


def generate_firestore_id_from_doi(doi: str) -> str:
    """
    Generates a Firestore-friendly ID from a DOI by encoding it with base64.

    Args:
        doi (str): The DOI of the paper.

    Returns:
        str: A base64-encoded representation of the DOI, suitable for use as a Firestore document ID.
    """
    return base64.urlsafe_b64encode(doi.encode("utf-8")).decode("utf-8").rstrip("=")


def get_paper_library_service(user_id: str) -> list[Paper]:
    """
    Retrieves a list of papers for a given user from Firestore.

    Args:
        user_id (str): The ID of the user whose paper library is to be fetched.

    Returns:
        list[Paper]: A list of Paper objects retrieved from the user's Firestore library.
    """
    papers_ref = db.collection("users").document(user_id).collection("papers")
    papers = papers_ref.stream()
    paper_list = []
    for paper in papers:
        paper_dict = paper.to_dict()
        paper_list.append(Paper(**paper_dict))
    return paper_list


def save_paper_library_service(user_id: str, paper_data: list[Paper]) -> None:
    """
    Saves or updates a list of papers for a given user in Firestore.
    Existing papers not in the provided list are deleted.

    Args:
        user_id (str): The ID of the user whose paper library is to be saved.
        paper_data (list[Paper]): A list of Paper objects to be saved or updated in the user's library.

    Returns:
        None
    """
    papers_ref = db.collection("users").document(user_id).collection("papers")
    saved_papers = papers_ref.stream()
    ids_to_keep = [generate_firestore_id_from_doi(paper.doi) for paper in paper_data]
    for paper in saved_papers:
        if paper.id not in ids_to_keep:
            papers_ref.document(paper.id).delete()
    for paper in paper_data:
        paper_id = generate_firestore_id_from_doi(paper.doi)
        papers_ref.document(paper_id).set(paper.model_dump())
