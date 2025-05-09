from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.papers import get_paper_library_service
from app.services.recommended import get_paper_recommendations_service
from app.schemas.papers import Paper


router = APIRouter()


@router.get("", response_model=list[Paper])
def get_recommendations(user_id: str = Depends(get_current_user)):
    user_papers = get_paper_library_service(user_id)
    recommended_papers = get_paper_recommendations_service(user_papers)
    return recommended_papers
