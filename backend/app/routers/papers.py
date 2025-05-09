from fastapi import APIRouter, Depends, Query, HTTPException

from app.firebase import get_current_user
from app.services.papers import (
    get_paper_library_service,
    search_papers_service,
    add_paper_to_library_service,
    delete_paper_from_library_service,
)
from app.schemas.papers import Paper


router = APIRouter()


@router.get("/papers", response_model=list[Paper])
def get_paper_library(user_id: str = Depends(get_current_user)) -> list[Paper]:
    """
    Retrieves a list of papers for a given user from Firestore.
    Note that a valid user_id is needed to call this function.

    Args:
        user_id (str): The ID of the user whose paper library is to be fetched.

    Returns:
        list[Paper]: A list of Paper objects retrieved from the user's Firestore library.
    """
    return get_paper_library_service(user_id)


# @router.post("/papers")
# def save_paper_library(
#     paper_data: list[Paper], user_id: str = Depends(get_current_user)
# ):
#     return save_paper_library_service(user_id, paper_data)


@router.post("/papers/add", response_model=Paper)
def add_paper_to_library(paper: Paper, user_id: str = Depends(get_current_user)):
    """
    Add a single paper to the user's library.

    Args:
        paper (Paper): The paper to add to the library
        user_id (str): The ID of the current user

    Returns:
        Paper: The added paper
    """
    try:
        add_paper_to_library_service(user_id, paper)
        return paper
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add paper to library: {str(e)}"
        )


@router.delete("/papers/{paper_id}")
def delete_paper_from_library(paper_id: str, user_id: str = Depends(get_current_user)):
    """
    Delete a single paper from the user's library.

    Args:
        paper_id (str): The ID of the paper to delete
        user_id (str): The ID of the current user

    Returns:
        dict: A message confirming the deletion
    """
    try:
        delete_paper_from_library_service(user_id, paper_id)
        return {"message": f"Paper {paper_id} successfully deleted from library"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete paper from library: {str(e)}"
        )


@router.get("/search", response_model=list[Paper])
def search_papers(
    query: str = Query(..., description="The search query string"),
    limit: int = Query(
        5, ge=1, le=100, description="Maximum number of results to return"
    ),
):
    """
    Search for papers using the Semantic Scholar API.

    Args:
        query (str): The search query string
        limit (int): Maximum number of results to return (default: 5)

    Returns:
        list[Paper]: List of papers matching the search query
    """
    return search_papers_service(
        query=query,
        limit=limit,
    )
