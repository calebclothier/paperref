from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.graph import get_graph_service
from app.schemas.papers import Paper
from app.schemas.graph import GraphResponse


router = APIRouter()


@router.post("", response_model=GraphResponse)
def get_graph(paper: Paper, user_id: str = Depends(get_current_user)):
    return get_graph_service(paper, user_id)
