import requests
import time

from fastapi import HTTPException

from app.config import settings
from app.schemas.papers import Paper, PaperDetail
from app.schemas.graph import Node, Edge, DirectedGraph, GraphResponse


import requests
from math import ceil
from fastapi import HTTPException

class PaperBatchFetcher:
    """Fetches paper details in batches from the Semantic Scholar API."""
    
    BASE_URL = f"{settings.SEMANTIC_SCHOLAR_API_URL}/paper/batch"
    FIELDS = [
        "externalIds", 
        "title", 
        "authors", 
        "abstract", 
        "year",
        "referenceCount", 
        "citationCount", 
        "publicationVenue",
        "openAccessPdf"]
    TOP_LEVEL_FIELDS = [
        "citations",
        "references",
        "tldr"]

    def __init__(self):
        self.headers = {"Content-Type": "application/json; charset=UTF-8"}
        all_fields = self.FIELDS + self.TOP_LEVEL_FIELDS + self._get_nested_fields()
        self.params = {"fields": ",".join(all_fields)}

    @staticmethod
    def _get_nested_fields():
        """Generate nested fields for citations and references."""
        return [f"{relation}.{field}" for relation in ("citations", "references") for field in PaperBatchFetcher.FIELDS]

    def fetch(self, paper_ids):
        """Fetch details for a list of paper IDs (up to 50 at a time)."""
        payload = {"ids": paper_ids}
        try:
            response = requests.post(
                self.BASE_URL, 
                headers=self.headers, 
                params=self.params, 
                json=payload, 
                timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching paper data: {e}")

    def fetch_batched(self, paper_ids, batch_size=50):
        """Fetch details for a list of paper IDs in batches to avoid size limits."""
        results = []
        num_batches = ceil(len(paper_ids) / batch_size)
        for i in range(num_batches):
            batch_ids = paper_ids[i * batch_size : (i + 1) * batch_size]
            try:
                batch_results = self.fetch(batch_ids)
                results.extend(batch_results)
                time.sleep(1)
            except HTTPException as error:
                raise HTTPException(status_code=500, detail=error.detail)
        return results


class BaseGraphBuilder:
    """Base class for constructing directed graphs from paper data."""

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, paper_data):
        """Add a node to the graph if it doesn’t already exist."""
        paper_id = paper_data["paperId"]
        if paper_id not in self.nodes:
            self.nodes[paper_id] = Node(id=paper_id, detail=PaperDetail(**parse_paper_detail(paper_data)))
        elif not self.nodes[paper_id].detail.tldr and isinstance(paper_data['tldr'], dict):
            self.nodes[paper_id].detail.tldr = paper_data['tldr']['text']

    def add_edge(self, source_id, target_id):
        """Add an edge between two nodes"""
        self.edges.append(Edge(source=source_id, target=target_id))

    def build_graph_response(self):
        """Build and return the graph."""
        return DirectedGraph(
            nodes=list(self.nodes.values()), 
            edges=self.edges, 
            max_citations=self._max_citations())

    def _max_citations(self):
        """Calculate the maximum citation count among all nodes."""
        return max((node.detail.citation_count for node in self.nodes.values()), default=0)


class CitationGraphBuilder(BaseGraphBuilder):
    """Constructs a directed citation graph from paper data."""

    def add_paper_and_edges(self, source_paper, include_new_nodes=True):
        """Add a paper and its citation edges."""
        self.add_node(source_paper)
        source_id = source_paper["paperId"]
        for citation_paper in source_paper.get("citations", []):
            citation_id = citation_paper.get("paperId")
            if not citation_id:
                continue
            if citation_id in self.nodes:
                self.add_edge(source_id, citation_id)
            elif include_new_nodes:
                self.add_node(citation_paper)
                self.add_edge(source_id, citation_id)


class ReferenceGraphBuilder(BaseGraphBuilder):
    """Constructs a directed reference graph from paper data."""

    def add_paper_and_edges(self, source_paper, include_new_nodes=True):
        """Add a paper and its reference edges."""
        self.add_node(source_paper)
        source_id = source_paper["paperId"]
        for reference_paper in source_paper.get("references", []):
            reference_id = reference_paper.get("paperId")
            if not reference_id:
                continue
            if reference_id in self.nodes:
                self.add_edge(reference_id, source_id)
            elif include_new_nodes:
                self.add_node(reference_paper)
                self.add_edge(reference_id, source_id)


def get_graph_service(paper: Paper, user_id: str):
    """Fetch papers and build citation and reference graphs for the given user."""
    fetcher = PaperBatchFetcher()
    citation_builder = CitationGraphBuilder()
    reference_builder = ReferenceGraphBuilder()
    # Initial batch fetch for input papers
    initial_id = f"DOI:{paper.doi}"
    initial_papers = fetcher.fetch([initial_id])
    # Process initial papers and their first-level citations and references
    for paper in initial_papers:
        citation_builder.add_paper_and_edges(paper, include_new_nodes=True)
        reference_builder.add_paper_and_edges(paper, include_new_nodes=True)
    # Second-level fetch to find connections between existing nodes
    time.sleep(1)  # sleep to avoid API rate limits
    top_50_ids = [
        node_id for node_id, node in sorted(
            citation_builder.nodes.items(),
            key=lambda item: item[1].detail.citation_count,
            reverse=True)[:50]]
    second_level_papers = fetcher.fetch(top_50_ids)
    # Process second-level papers, adding edges between existing nodes only
    for paper in second_level_papers:
        paper_id = paper['paperId']
        if paper_id in citation_builder.nodes:
            citation_builder.add_paper_and_edges(paper, include_new_nodes=False)
        if paper_id in reference_builder.nodes:
            reference_builder.add_paper_and_edges(paper, include_new_nodes=False)
    return GraphResponse(
        citation_graph=citation_builder.build_graph_response(),
        reference_graph=reference_builder.build_graph_response())


def parse_paper_detail(paper):
    """Utility function to parse paper details using the global fields."""
    external_ids = paper['externalIds']
    open_access = paper['openAccessPdf']
    publication_venue = paper['publicationVenue']
    doi = None
    arxiv = None
    journal = None
    open_access_url = None
    tldr = None
    if isinstance(external_ids, dict):
        doi = external_ids.get('DOI', None)
        arxiv = external_ids.get('ArXiv', None)
    if isinstance(publication_venue, dict):
        journal = publication_venue.get('name', '')
    if isinstance(open_access, dict):
        open_access_url = open_access.get('url', None)
    if isinstance(paper.get('tldr', None), dict):
        tldr = paper['tldr'].get('text')
    return {
        'doi': doi,
        'arxiv': arxiv,
        'title': paper['title'],
        'authors': [author['name'] for author in paper['authors']],
        'abstract': paper['abstract'],
        'year': paper['year'],
        'reference_count': paper['referenceCount'],
        'citation_count': paper['citationCount'],
        'journal': journal,
        'open_access_url': open_access_url,
        'tldr': tldr}
