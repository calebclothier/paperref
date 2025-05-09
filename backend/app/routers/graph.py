from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.graph import get_graph_service, get_references_service, get_citations_service
from app.schemas.papers import Paper
from app.schemas.graph import GraphResponse


router = APIRouter()


@router.post("", response_model=GraphResponse)
def get_graph(paper: Paper, user_id: str = Depends(get_current_user)):
    return get_graph_service(paper)


@router.post("/references", response_model=list[Paper])
def get_references(papers: list[Paper], user_id: str = Depends(get_current_user)):
    return get_references_service(papers)


@router.post("/citations", response_model=list[Paper])
def get_citations(papers: list[Paper], user_id: str = Depends(get_current_user)):
    return get_citations_service(papers)


