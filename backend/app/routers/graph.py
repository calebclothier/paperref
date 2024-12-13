"""Routers for graph modules"""

from fastapi import APIRouter, Depends

from app.firebase import get_current_user
from app.services.graph import get_graph_service
from app.schemas.papers import Paper
from app.schemas.graph import GraphResponse


router = APIRouter()


@router.post("", response_model=GraphResponse)
def get_graph(paper: Paper, user_id: str = Depends(get_current_user)) -> GraphResponse:
    """
    Fetch a paper and build a citation and reference graphs for a given user.
    Note that a valid user_id is needed to call this function.

    Args:
        paper (Paper): The paper from which to generate the graphs.
        user_id (str): The ID of the user

    Returns:
        GraphResponse: The object containing the citation and reference graphs.
    """
    return get_graph_service(paper)
