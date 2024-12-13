"""Routers for paper recommendation modules"""

from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.papers import get_paper_library_service
from app.services.recommended import get_paper_recommendations_service
from app.schemas.papers import PaperDetail


router = APIRouter()


@router.get("", response_model=list[PaperDetail])
def get_recommendations(user_id: str = Depends(get_current_user)) -> list[PaperDetail]:
    """
    Retrieves a list of recommended papers for a given user.
    Note that a valid user_id is needed to call this function.

    Args:
        user_id (str): The ID of the user whose paper library has to generate a recommendation list.

    Returns:
        list[PaperDetail]: A list of PaperDetail objects retrieved from the user's paper library.

    Raises:
        HTTPException: Any error that occurs during authentication.
    """
    user_papers = get_paper_library_service(user_id)
    recommended_papers = get_paper_recommendations_service(user_papers)
    return recommended_papers
