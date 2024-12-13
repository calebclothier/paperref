import requests

import streamlit as st

from src.api.auth import check_id_token


def get_graph_for_paper(selected_paper: dict):
    # check and refresh id_token if necessary
    check_id_token()
    # backend POST request
    url = f"{st.secrets['backend']['url']}/graph"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    try:
        # Perform POST request to fetch graph data
        response = requests.post(url, headers=headers, json=selected_paper, timeout=60)
        # Handle errors
        if response.status_code != 200:
            st.error("Unable to fetch citation graphs.")
            return None
        # Process graph data
        response = response.json()
        citation_graph = parse_graph_to_cytoscape_elements(response["citation_graph"])
        reference_graph = parse_graph_to_cytoscape_elements(response["reference_graph"])
        result = {
            "citation_graph": response["citation_graph"],
            "reference_graph": response["reference_graph"],
            "citation_graph_cytoscape": citation_graph,
            "reference_graph_cytoscape": reference_graph,
        }
        return result
    except requests.exceptions.RequestException:
        st.error("Unable to fetch citation graphs.")
    return None


def parse_graph_to_cytoscape_elements(graph: dict):
    elements = []
    # Process nodes from the citation graph
    for node in graph["nodes"]:
        detail = node["detail"]
        # Filter out None values and build the data dictionary for the Cytoscape element
        node_data = {key: value for key, value in detail.items() if value is not None}
        authors = node_data["authors"]
        if authors and isinstance(authors, list):
            first_author = authors[0].split(" ")[-1]
        else:
            first_author = ""
        year = str(node_data.get("year", ""))
        node_data["label"] = ", ".join([first_author, year]) if year else first_author
        node_data["id"] = node["id"]  # Ensure the node ID is included
        # Cytoscape element for the node
        elements.append({"data": node_data, "selectable": True, "selected": False})
    # Process edges from the citation graph
    for edge in graph["edges"]:
        elements.append(
            {
                "data": {
                    "source": edge["source"],
                    "target": edge["target"],
                    "id": f"{edge['source']}-{edge['target']}",
                }
            }
        )
    return elements
