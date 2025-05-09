from datetime import datetime
import re

import streamlit as st

# NOTE: config must be before module-level imports
st.set_page_config(page_title="Citation Graph", page_icon="💠", layout="wide")
from st_cytoscape import cytoscape

from src.api.auth import check_cookie
from src.api.library import get_library
from src.api.graph import get_graph_for_paper


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png",
)


# check authentication
check_cookie()
# if not authenticated, stop page rendering
if not st.session_state.get("authenticated", False):
    st.error("You must be logged in to view this page.")
    st.stop()


# load paper library if not in session_state
if st.session_state.get("papers_df", None) is None:
    st.session_state.papers_df = get_library()


# inject markdown for custom page styling
st.markdown(
    """
    <style>
        /* Remove padding on the main block container */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Remove padding from specific containers with precise control */
        .st-key-search_container, .st-key-graph_container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin: 0 !important; /* Ensures no extra space from margins */
        }

        /* Optional: Set padding only where necessary */
        .st-key-search_container {
            padding-top: 1.5rem !important;
            padding-left: 8rem !important;
            padding-right: 8rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# top-of-page selector for configuring citation graph
with st.container(key="search_container"):
    col1, col2, col3 = st.columns([0.6, 0.15, 0.25], vertical_alignment="bottom")
    # select the paper for the citation graph
    options = st.session_state.get("papers_df").rename(
        columns={"DOI": "doi", "Title": "title"}
    )
    options = options.to_dict(orient="records")
    selected_paper = col1.selectbox(
        label="Select paper:", options=options, format_func=lambda row: row["title"]
    )
    # button to build graph
    if col2.button(label="Build", use_container_width=True):
        # load graph from backend
        data = get_graph_for_paper(selected_paper)
        # save graph data to session state
        st.session_state.citation_graph = data["citation_graph"]
        st.session_state.citation_graph_cytoscape = data["citation_graph_cytoscape"]
        st.session_state.reference_graph = data["reference_graph"]
        st.session_state.reference_graph_cytoscape = data["reference_graph_cytoscape"]
    # radio selector to toggle between citation graph or reference graph
    graph_type = col3.radio("Graph type:", ["Citations", "References"], horizontal=True)
    graph_key = "citation_graph" if graph_type == "Citations" else "reference_graph"

# graph container
with st.container(key="graph_container"):
    if st.session_state.get(graph_key, None):
        # compute max and min publication date in graph
        years = [
            node["data"].get("year", datetime.now().year)
            for node in st.session_state.get(f"{graph_key}_cytoscape")
        ]
        min_year = min(years)
        max_year = max(years)
        # compute max and min citation count in graph
        citations = [
            node["data"].get("citation_count", 0)
            for node in st.session_state.get(f"{graph_key}_cytoscape")
        ]
        min_citations = min(citations)
        max_citations = max(citations)
        # graph styling
        stylesheet = [
            {
                "selector": "node",
                "style": {
                    "label": "data(label)",
                    "color": "#fff",
                    "font-size": "4px",
                    "text-valign": "center",
                    "text-halign": "center",
                    "height": f"mapData(citation_count, {min_citations}, {max_citations}, 10px, 120px)",
                    "width": f"mapData(citation_count, {min_citations}, {max_citations}, 10px, 120px)",
                    "background-color": "#30c9bc",
                    "background-opacity": f"mapData(year, {min_year}, {max_year}, 0.1, 1)",
                    "border-color": "#fff",
                    "border-width": "0.5px",
                },
            },
            {
                "selector": "edge",
                "style": {"width": 0.25, "line-color": "#ccc", "line-opacity": 0.5},
            },
        ]
        # cytoscape graph object
        st.session_state.graph_selection = cytoscape(
            st.session_state.get(f"{graph_key}_cytoscape"),
            stylesheet,
            key="graph",
            height="600px",
            width="100%",
            selection_type="single",
            layout={
                "name": "fcose",
                "fit": True,
                "animate": True,
                "pan": {"x": "200px", "y": "200px"},
            },
        )


def clean_title(text: str):
    """Helper function that cleans up paper titles for markdown display."""
    # Remove the outer MathML tag
    text = re.sub(r"<mml:math[^>]*>|</mml:math>", "", text)
    # Remove individual tags but keep their content
    text = re.sub(r"<mml:[a-z]+>|</mml:[a-z]+>", "", text)
    # Remove self-closing tags like <mml:mprescripts /> and <mml:none />
    text = re.sub(r"<mml:[a-z]+ ?/>", "", text)
    # Handle any leftover inline elements that may need closing
    text = re.sub(r"[\n\r]", "", text)  # Remove newlines
    return text.strip()


# sidebar for displaying node details
with st.sidebar:
    # paper description
    if st.session_state.get("graph_selection", None) is not None:
        selected_nodes = st.session_state.graph_selection["nodes"]
        if len(selected_nodes) > 0:
            node_id = selected_nodes[0]
            node_detail = [
                node["detail"]
                for node in st.session_state.get(graph_key)["nodes"]
                if node["id"] == node_id
            ][0]
            # display title
            title = clean_title(node_detail["title"])
            st.markdown(f"### {title}")
            # display authors
            if len(node_detail["authors"]) > 10:
                with st.expander(label=f"{node_detail['authors'][0]} _et al._"):
                    st.markdown(", ".join(node_detail["authors"]))
            else:
                st.markdown(", ".join(node_detail["authors"]))
            # display journal and year
            if node_detail["journal"]:
                st.markdown(f"{node_detail['year']}, _{node_detail['journal']}_")
            else:
                st.markdown(f"{node_detail['year']}")
            # display citation count
            st.markdown(f"{node_detail['citation_count']} Citations")
            # display links
            if node_detail["arxiv"]:
                col1, col2, _ = st.columns([0.2, 0.2, 0.6])
                col1.link_button(
                    label="",
                    help="PDF",
                    icon=":material/picture_as_pdf:",
                    url=f"https://arxiv.org/pdf/{node_detail['arxiv']}",
                    use_container_width=True,
                )
                col2.link_button(
                    label="**X**",
                    help="ArXiv",
                    url=f"https://arxiv.org/abs/{node_detail['arxiv']}",
                    use_container_width=True,
                )
            # display TLDR or abstract
            if node_detail["tldr"]:
                st.markdown(f"_TLDR_: {node_detail['tldr'] or ''}")
            elif node_detail["abstract"]:
                st.markdown(f"{node_detail['abstract']}")
