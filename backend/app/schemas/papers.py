from pydantic import BaseModel
from typing import Optional


class Paper(BaseModel):
    doi: str
    title: str
    
    
class PaperDetail(BaseModel):
    doi: Optional[str] = None
    arxiv: Optional[str] = None
    title: str
    authors: list[str]
    abstract: Optional[str] = None
    year: Optional[int] = None
    reference_count: Optional[int] = None
    citation_count: Optional[int] = None
    journal: Optional[str] = None
    open_access_url: Optional[str] = None
    tldr: Optional[str] = None
    
    