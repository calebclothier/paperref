"""Graph services to fetch, load and parse paper data to build citation and reference graphs."""

import requests
import time
from math import ceil

from fastapi import HTTPException

from app.config import settings
from app.schemas.papers import Paper
from app.schemas.graph import Node, Edge, DirectedGraph, GraphResponse
from app.utils.paper import parse_paper_detail


class PaperBatchFetcher:
    """
    Fetches paper details in batches from the Semantic Scholar API.

    Attributes:
        FIELDS (list[str]): Miscellaneous fields including the paper's
                            abstract, title, number of citations, number
                            of references.
        TOP_LEVEL_FIELDS (list[str]): Miscellaneous important fields including
                            the paper's list of papers that cite it, list of
                            reference papers, and a list of AI generated summaries
                            for each.
    """

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
        "openAccessPdf",
    ]
    TOP_LEVEL_FIELDS = ["citations", "references", "tldr"]
    HEADERS = {"Content-Type": "application/json; charset=UTF-8"}

    def __init__(self):
        self.all_fields = (
            self.FIELDS
            + self.TOP_LEVEL_FIELDS
            + self._get_nested_fields(["citations", "references"])
        )
        self.citation_fields = (
            self.FIELDS + self.TOP_LEVEL_FIELDS + self._get_nested_fields(["citations"])
        )
        self.reference_fields = (
            self.FIELDS
            + self.TOP_LEVEL_FIELDS
            + self._get_nested_fields(["references"])
        )

    @staticmethod
    def _get_nested_fields(keys_to_nest: list[str]) -> list[str]:
        """
        Generate nested fields for citations and references.

        Args:
            keys_to_nest (list[str]): The keys to nest over for the class fields.

        Returns:
            list[str]: A list of strings for the nested keys and fields
        """
        return [
            f"{relation}.{field}"
            for relation in keys_to_nest
            for field in PaperBatchFetcher.FIELDS
        ]

<<<<<<< HEAD
    def fetch(self, paper_ids: list[str], key="both") -> dict:
        """Fetch details for a list of paper IDs (up to 50 at a time)."""
=======
    def fetch(self, paper_ids: list[int], key="both") -> dict:
        """
        Fetch details for a list of paper IDs (up to 50 at a time).

        Args:
            paper_ids (list[int]): List of paper ID's
            key (str): Which data to fetch; must be either 'both', 'citations' or 'references'

        Returns:
            dict: The data for the list of papers, determined by the key

        Raises:
            HTTPException: Any error fetching paper data
        """
>>>>>>> d0be991 (add: added docstrings and static typying (#15))
        payload = {"ids": paper_ids}
        if key == "both":
            fields = self.all_fields
        elif key == "citations":
            fields = self.citation_fields
        elif key == "references":
            fields = self.reference_fields
        elif key == "none":
            fields = self.FIELDS
        else:
            raise ValueError(
                'Invalid fetch key: must be one of ["both", "citations", "references", "none"]'
            )
        params = {"fields": ",".join(fields)}
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.HEADERS,
                params=params,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching paper data: {e}"
            )

<<<<<<< HEAD
    def fetch_batched(self, paper_ids: list[str], batch_size=50, key="both") -> list[dict]:
        """Fetch details for a list of paper IDs in batches to avoid size limits."""
=======
    def fetch_batched(self, paper_ids: list[int], batch_size=50) -> list[dict]:
        """
        Fetch details for a list of paper IDs in batches to avoid size limits.
        Uses key='both' for fetch function.

        Args:
            paper_ids (list[int]): List of paper ID's
            batch_size (int): Batch size to fetch a list of papers

        Returns:
            list[dict]: The batched data for the list of papers.

        Raises:
            HTTPException: Any error fetching paper data
        """
>>>>>>> d0be991 (add: added docstrings and static typying (#15))
        results = []
        num_batches = ceil(len(paper_ids) / batch_size)
        for i in range(num_batches):
            batch_ids = paper_ids[i * batch_size : (i + 1) * batch_size]
            try:
                batch_results = self.fetch(batch_ids, key=key)
                results.extend(batch_results)
                time.sleep(1)
            except HTTPException as error:
                raise HTTPException(status_code=500, detail=error.detail)
        return results


class BaseGraphBuilder:
    """
    Base class for constructing directed graphs from paper data.

    Attributes:
        nodes (dict): assigns a paper's "paperId" str to a app.schemas.graph.Node object
        edges (list): assigns edges as app.schemas.graph.Edge objects
    """

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, paper_data: dict):
<<<<<<< HEAD
        """Add a node to the graph if it doesn't already exist."""
=======
        """
        Add a node to the graph if it doesn’t already exist.

        Args:
            paper_data (dict): Data dictionary for a given paper

        Returns:
            None

        """
>>>>>>> d0be991 (add: added docstrings and static typying (#15))
        paper_id = paper_data["paperId"]
        if paper_id not in self.nodes:
            self.nodes[paper_id] = Node(
                id=paper_id, detail=Paper(**parse_paper_detail(paper_data))
            )
        elif not self.nodes[paper_id].detail.tldr and isinstance(
            paper_data["tldr"], dict
        ):
            self.nodes[paper_id].detail.tldr = paper_data["tldr"]["text"]

    def add_edge(self, source_id: str, target_id: str):
        """
        Add an edge between two nodes

        Args:
            source_id (str): Source paper's ID
            target_id (str): Target paper's ID

        Returns:
            None
        """
        self.edges.append(Edge(source=source_id, target=target_id))

    def build_graph_response(self) -> DirectedGraph:
        """
        Build and return the graph.

        Args:
            None

        Returns:
            DirectedGraph
        """
        return DirectedGraph(
            nodes=list(self.nodes.values()),
            edges=self.edges,
            max_citations=self._max_citations(),
        )

    def _max_citations(self) -> int:
        """
        Calculate the maximum citation count among all nodes.

        Args:
            None

        Returns:
            int
        """
        return max(
            (node.detail.citation_count for node in self.nodes.values()), default=0
        )


class CitationGraphBuilder(BaseGraphBuilder):
    """
    Constructs a directed citation graph from paper data.
    Inherits from BaseGraphBuilder.

    Attributes:
        (see BaseGraphBuilder)
    """

    def add_paper_and_edges(
        self, source_paper: Paper, include_new_nodes=True, num_nodes=-1
    ):
        """
        Add a paper and its citation edges.

        Args:
            source_paper (Paper): input paper
            include_new_nodes (bool): Boolean to include new nodes in the graph from the citations
            num_nodes (int): if -1 then add all citations, otherwise add top num_nodes most cited papers

        Returns:
            None
        """
        # First create an ordered list of citations based on their "citationCount"
        ordered_citations = [
            citation_paper
            for citation_paper in sorted(
                source_paper.get("citations", []),
                key=lambda item: item["citationCount"]
                if item["citationCount"] is not None
                else 0,
                reverse=True,
            )
        ]
        # Keep the top num_nodes most cited papers in the citations
        if num_nodes != -1:
            ordered_citations = ordered_citations[:num_nodes]
        # Add original paper
        self.add_node(source_paper)
        source_id = source_paper["paperId"]
        # Add citation papers
        for citation_paper in ordered_citations:
            citation_id = citation_paper.get("paperId")
            if not citation_id:
                continue
            if citation_id in self.nodes:
                self.add_edge(source_id, citation_id)
            elif include_new_nodes:
                self.add_node(citation_paper)
                self.add_edge(source_id, citation_id)


class ReferenceGraphBuilder(BaseGraphBuilder):
    """
    Constructs a directed reference graph from paper data.

    Attributes:
        (see BaseGraphBuilder)
    """

<<<<<<< HEAD
    def add_paper_and_edges(
        self, source_paper: Paper, include_new_nodes=True, num_nodes=-1
    ):
        """Add a paper and its reference edges.

        Args:
            source_paper (Paper): input paper
            include_new_nodes (bool): Boolean to include new nodes in the graph from the references
            num_nodes (int): if -1 then add all references, otherwise add top num_nodes most cited papers
        """

=======
    def add_paper_and_edges(self, source_paper, include_new_nodes=True, num_nodes=-1):
        """
        Add a paper and its reference edges.

        Args:
            source_paper (Paper): input paper
            include_new_nodes (bool): Boolean to include new nodes in the graph from the citations
            num_nodes (int): if -1 then add all citations, otherwise add top num_nodes most cited papers

        Returns:
            None
        """
>>>>>>> d0be991 (add: added docstrings and static typying (#15))
        # First create an ordered list of references based on their "citationCount"
        ordered_references = [
            reference_paper
            for reference_paper in sorted(
                source_paper.get("references", []),
                key=lambda item: item["citationCount"]
                if item["citationCount"] is not None
                else 0,
                reverse=True,
            )
        ]
        # Keep the top num_nodes most cited papers in the references
        if num_nodes != -1:
            ordered_references = ordered_references[:num_nodes]
        # Add original paper
        self.add_node(source_paper)
        source_id = source_paper["paperId"]
        # Add reference papers
        for reference_paper in ordered_references:
            reference_id = reference_paper.get("paperId")
            if not reference_id:
                continue
            if reference_id in self.nodes:
                self.add_edge(reference_id, source_id)
            elif include_new_nodes:
                self.add_node(reference_paper)
                self.add_edge(reference_id, source_id)


def get_graph_service(paper: Paper, num_nodes=20) -> GraphResponse:
    """Fetch papers and build citation and reference graphs for the given user.
    Args:
        paper (Paper): Input paper
        num_nodes (int): Number of papers (ordered by their number of citations) to keep
                        in the citation graph of the input paper

    Returns:
        GraphResponse: Returns both citation and reference graphs as DirectedGraph objects
                        wrapped in a GraphResponse object
    """

    fetcher = PaperBatchFetcher()
    citation_builder = CitationGraphBuilder()
    reference_builder = ReferenceGraphBuilder()
    # Initial batch fetch for input papers
    initial_papers = fetcher.fetch([paper.id], key="both")

    # Add to citation_builder the top num_nodes most cited papers that cite it
    for paper in initial_papers:
        citation_builder.add_paper_and_edges(
            paper, include_new_nodes=True, num_nodes=num_nodes
        )
        reference_builder.add_paper_and_edges(
            paper, include_new_nodes=True, num_nodes=num_nodes
        )

    # Second-level fetch to find connections between existing nodes
    cited_papers_to_fetch = list(citation_builder.nodes.keys())
    reference_papers_to_fetch = list(reference_builder.nodes.keys())

    # Avoid fetching papers with too many citations or references
    max_citations = 500
    max_references = 500
    cited_papers_to_fetch = [
        paper_id
        for paper_id in cited_papers_to_fetch
        if citation_builder.nodes[paper_id].detail.citation_count < max_citations
    ]
    reference_papers_to_fetch = [
        paper_id
        for paper_id in reference_papers_to_fetch
        if reference_builder.nodes[paper_id].detail.reference_count < max_references
    ]

    # Fetch additional papers if needed
    if cited_papers_to_fetch:
        citation_papers = fetcher.fetch_batched(cited_papers_to_fetch, key="citations")
        for paper in citation_papers:
            citation_builder.add_paper_and_edges(
                paper, include_new_nodes=False, num_nodes=num_nodes
            )

    if reference_papers_to_fetch:
        reference_papers = fetcher.fetch_batched(reference_papers_to_fetch, key="references")
        for paper in reference_papers:
            reference_builder.add_paper_and_edges(
                paper, include_new_nodes=False, num_nodes=num_nodes
            )

    return GraphResponse(
        citation_graph=citation_builder.build_graph_response(),
        reference_graph=reference_builder.build_graph_response(),
    )
    
    
def get_references_service(papers: list[Paper]) -> list[Paper]:
    """Get references for a list of papers."""
    paper_ids = [paper.id for paper in papers]
    fetcher = PaperBatchFetcher()
    results = fetcher.fetch_batched(paper_ids, key="references")
    references = [ref for paper in results for ref in paper.get("references", []) if ref['paperId']]
    return [Paper(**parse_paper_detail(ref)) for ref in references]


def get_citations_service(papers: list[Paper]) -> list[Paper]:
    """Get references for a list of papers."""
    paper_ids = [paper.id for paper in papers]
    fetcher = PaperBatchFetcher()
    results = fetcher.fetch_batched(paper_ids, key="citations")
    citations = [citation for paper in results for citation in paper.get("citations", []) if citation['paperId']]
    return [Paper(**parse_paper_detail(citation)) for citation in citations]
