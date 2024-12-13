"""Routers for paper loading, saving and updating
"""
from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.papers import get_paper_library_service, save_paper_library_service
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


@router.post("/papers")
def save_paper_library(paper_data: list[Paper], user_id: str = Depends(get_current_user)) -> None:
    """
    Saves or updates a list of papers for a given user in Firestore. 
    Existing papers not in the provided list are deleted.
    Note that a valid user_id is needed to call this function.

    Args:
        paper_data (list[Paper]): A list of Paper objects to be saved or updated in the user's library.
        user_id (str): The ID of the user whose paper library is to be saved.

    Returns:
        None
    """
    return save_paper_library_service(user_id, paper_data)
