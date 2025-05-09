from pydantic import BaseModel

from app.schemas.papers import Paper


class Node(BaseModel):
    id: str  # Unique identifier for the node
    detail: Paper


class Edge(BaseModel):
    source: str  # The id of the source node
    target: str  # The id of the target node


class DirectedGraph(BaseModel):
    nodes: list[Node]  # List of nodes in the graph
    edges: list[Edge]  # List of directed edges in the graph
    max_citations: int


class GraphResponse(BaseModel):
    citation_graph: DirectedGraph
    reference_graph: DirectedGraph
