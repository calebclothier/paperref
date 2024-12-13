from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.papers import get_paper_library_service, save_paper_library_service
from app.schemas.papers import Paper


router = APIRouter()


@router.get("/papers", response_model=list[Paper])
def get_paper_library(user_id: str = Depends(get_current_user)):
    return get_paper_library_service(user_id)


@router.post("/papers")
def save_paper_library(
    paper_data: list[Paper], user_id: str = Depends(get_current_user)
):
    return save_paper_library_service(user_id, paper_data)
