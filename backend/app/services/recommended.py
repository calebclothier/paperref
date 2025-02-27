"""Recommended paper services for generating a user's recommended papers list based on a list of user input papers."""

import requests
from fastapi import HTTPException

from app.schemas.papers import Paper, PaperDetail


def get_paper_recommendations_service(user_papers: list[Paper]) -> list[PaperDetail]:
    """
    Generates a list of recommended papers based on an input list of user papers.

    Args:
        user_papers (list[Paper]): List of papers from the user

    Returns:
        list[PaperDetail]: List of recommended papers (with detailed data)

    Raises:
        HTTPException: Raises any exception during recommendation fetching
    """
    paper_ids = [f"DOI:{paper.doi}" for paper in user_papers]
    payload = {"positivePaperIds": paper_ids, "negativePaperIds": []}
    base_url = "https://api.semanticscholar.org/recommendations/v1/papers"
    fields = ["title", "authors", "year", "publicationDate", "url", "citationCount"]
    full_url = base_url + "?fields=" + ",".join(fields)
    try:
        response = requests.post(
            url=full_url,
            headers={"content-type": "application/json; charset=UTF-8"},
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        response = response.json()
        papers = response["recommendedPapers"]
        return [PaperDetail(**parse_paper_detail(paper)) for paper in papers]
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching recommendations: {e}"
        )


def parse_paper_detail(paper: dict):
    """
    Utility function to parse paper details using the global fields.

    Args:
        paper (dict): Paper data dictionary

    Returns:
        None
    """
    return {
        "title": paper["title"],
        "authors": [author["name"] for author in paper["authors"]],
        "open_access_url": paper["url"],
        "year": paper["year"],
        "publication_date": paper["publicationDate"],
        "citation_count": paper["citationCount"],
    }
