"""Classes to manage the paper's citations and references
as directed graphs.
"""

from pydantic import BaseModel

from app.schemas.papers import Paper


class Node(BaseModel):
    id: str  # Unique identifier for the node
    detail: Paper


class Edge(BaseModel):
    """
    This class creates an edge object to represent a
    link between two nodes, and inherits from pydantic's
    BaseModel.

    Attributes:
        source (str): The id of the source node
        target (str): The id of the target node
    """
    source: str
    target: str


class DirectedGraph(BaseModel):
    """
    This class creates a graph object to represent a list of nodes and
    edges. Also inherits from pydantic's BaseModel.

    Attributes:
        nodes (list[Node]): List of nodes in the graph
        edges (list[Edge]): List of directed edges in the graph
        max_citations (int): maximum number of citations or edges
                             a single paper (node) can have
    """
    nodes: list[Node]
    edges: list[Edge]
    max_citations: int


class GraphResponse(BaseModel):
    """
    This class creates an object to represent a paper's citation graph
    and also a reference graph using the DirectedGraph object. Also
    inherits from pydantic's BaseModel.

    Attributes:
        citation_graph (DirectedGraph): Citation graph for a given paper
        reference_graph (DirectedGraph): Reference graph for a given paper
    """
    citation_graph: DirectedGraph
    reference_graph: DirectedGraph
