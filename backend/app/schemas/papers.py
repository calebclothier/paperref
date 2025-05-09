from pydantic import BaseModel
from typing import Optional


class PaperDetail(BaseModel):
    id: str
    title: str
    doi: Optional[str] = None
    arxiv: Optional[str] = None
    authors: Optional[list[str]] = None
    abstract: Optional[str] = None
    year: Optional[int] = None
    publication_date: Optional[str] = None
    reference_count: Optional[int] = None
    citation_count: Optional[int] = None
    journal: Optional[str] = None
    open_access_url: Optional[str] = None
    tldr: Optional[str] = None