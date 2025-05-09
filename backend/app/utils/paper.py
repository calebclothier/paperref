"""Utility functions for handling paper data."""

from typing import Optional


def parse_paper_detail(paper: dict) -> dict:
    """
    Parse paper details from a Semantic Scholar API response into a standardized format.
    
    Args:
        paper (dict): Raw paper data from Semantic Scholar API
        
    Returns:
        dict: Standardized paper data with all fields properly parsed
    """
    # Extract external IDs
    external_ids = paper.get("externalIds", {})
    doi = external_ids.get("DOI") if isinstance(external_ids, dict) else None
    arxiv = external_ids.get("ArXiv") if isinstance(external_ids, dict) else None
    
    # Extract publication venue
    publication_venue = paper.get("publicationVenue", {})
    journal = publication_venue.get("name") if isinstance(publication_venue, dict) else None
    
    # Extract open access URL
    open_access = paper.get("openAccessPdf", {})
    open_access_url = open_access.get("url") if isinstance(open_access, dict) else None
    
    # Extract TLDR
    tldr = paper.get("tldr", {}).get("text") if isinstance(paper.get("tldr"), dict) else None
    
    # Extract authors
    authors = [author.get("name", "") for author in paper.get("authors", [])]
    
    # Generate a unique ID from the DOI or paperId
    paper_id = paper.get("paperId") or doi
    
    return {
        "id": paper_id,
        "title": paper.get("title", ""),
        "doi": doi,
        "arxiv": arxiv,
        "authors": authors,
        "abstract": paper.get("abstract"),
        "year": paper.get("year"),
        "reference_count": paper.get("referenceCount"),
        "citation_count": paper.get("citationCount"),
        "journal": journal,
        "open_access_url": open_access_url,
        "tldr": tldr,
        "publication_date": paper.get("publicationDate"),
        "url": paper.get("url"),  # For recommendations API
    } 