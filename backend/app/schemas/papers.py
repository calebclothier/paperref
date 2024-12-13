"""Classes to manage the paper's data."""

from pydantic import BaseModel
from typing import Optional


class Paper(BaseModel):
    """
    This class creates a minimal object to represent a paper,
    and inherits from pydantic's BaseModel.

    Attributes:
        doi (str): Standard DOI identifier for the paper
        title (str): The paper's title
    """

    doi: str
    title: str


class PaperDetail(BaseModel):
    """
    This class creates a detailed object to represent a paper
    and its data, and also inherits from pydantic's BaseModel.

    Attributes:
        doi (str): Standard DOI identifier for the paper
        arxiv (str): The paper's arxiv url
        title (str): The paper's title
        authors (list[str]): The paper's author's
        abstract (Optional[str]): The paper's abstract
        year (Optional[int]): The paper's year of publication
        publication_date (Optional[str]): The paper's publication full date
        reference_count(Optional[str]): The number of references of the paper
        citation_count(Optional[int]): The number of papers that cite the paper
        journal(Optional[str]): The journal that published the paper
        open_access_url(Optional[str]): The journal's free url access for the paper
        tldr(Optional[str]): AI generated paper summary
    """

    doi: Optional[str] = None
    arxiv: Optional[str] = None
    title: str
    authors: list[str]
    abstract: Optional[str] = None
    year: Optional[int] = None
    publication_date: Optional[str] = None
    reference_count: Optional[int] = None
    citation_count: Optional[int] = None
    journal: Optional[str] = None
    open_access_url: Optional[str] = None
    tldr: Optional[str] = None
