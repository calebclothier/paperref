"""Paper services for managing a user's paper library in Firestore."""

import requests
import time
from fastapi import HTTPException

from app.database.firestore import db
from app.schemas.papers import Paper
from app.utils.paper import parse_paper_detail
from app.config import settings


def search_papers_service(
    query: str,
    limit: int = 5,
) -> list[Paper]:
    """
    Search for papers using the Semantic Scholar API.

    Args:
        query (str): The search query string
        limit (int): Maximum number of results to return (default: 5)

    Returns:
        list[Paper]: List of Paper objects matching the search query
    """
    base_url = f"{settings.SEMANTIC_SCHOLAR_API_URL}/paper/search"
    fields = [
        "paperId",
        "title",
        "authors",
        "abstract",
        "year",
        "publicationDate",
        "referenceCount",
        "citationCount",
        "publicationVenue",
        "openAccessPdf",
        "externalIds",
        "tldr",
    ]
    params = {
        "query": query,
        "limit": limit,
        "fields": ",".join(fields),
    }
    
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 429:  # Rate limit exceeded
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    raise HTTPException(
                        status_code=429,
                        detail="Semantic Scholar API rate limit exceeded. Please try again later."
                    )
            
            response.raise_for_status()
            data = response.json()
            papers = []
            for paper_data in data.get("data", []):
                paper = Paper(**parse_paper_detail(paper_data))
                papers.append(paper)
            return papers
            
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error searching papers: {e}"
                )
            time.sleep(retry_delay * (attempt + 1))


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


def add_paper_to_library_service(user_id: str, paper: Paper) -> None:
    """
    Adds a single paper to a user's library in Firestore.

    Args:
        user_id (str): The ID of the user whose library is to be updated.
        paper (Paper): The Paper object to be added to the library.

    Returns:
        None
    """
    papers_ref = db.collection("users").document(user_id).collection("papers")
    papers_ref.document(paper.id).set(paper.model_dump())


def delete_paper_from_library_service(user_id: str, paper_id: str) -> None:
    """
    Deletes a single paper from a user's library in Firestore.

    Args:
        user_id (str): The ID of the user whose library is to be updated.
        paper_id (str): The ID of the paper to be deleted.

    Returns:
        None
    """
    papers_ref = db.collection("users").document(user_id).collection("papers")
    papers_ref.document(paper_id).delete()
