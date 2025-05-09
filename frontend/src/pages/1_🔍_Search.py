import streamlit as st

# NOTE: config must be before module-level imports
st.set_page_config(page_title="Search Papers", page_icon="🔍", layout="wide")

from src.api.auth import check_cookie
from src.api.search import search_papers
from src.api.library import add_paper
from src.components.paper_display import display_paper


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


# Initialize session state for search results if not exists
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "last_search_query" not in st.session_state:
    st.session_state.last_search_query = ""


# Create a container for the search section
with st.container():
    # Create two columns for the search interface
    search_col, button_col = st.columns([0.8, 0.2], vertical_alignment='bottom')
    
    with search_col:
        # Search box
        search_query = st.text_input(
            "Search for papers",
            placeholder="Enter search terms...",
            key="search_query"
        )
    
    with button_col:
        # Search button
        button = st.button("Search", use_container_width=True)
        
        # Handle search button click
        if button:
            if search_query and search_query.strip():
                # Store the current search query
                st.session_state.last_search_query = search_query
                # Perform actual search using the API
                st.session_state.search_results = search_papers(search_query)
            else:
                st.warning("Please enter a search query.")

# Display results if they exist
if st.session_state.search_results:
    for idx, paper in enumerate(st.session_state.search_results):
        with st.container():
            display_paper(
                paper,
                show_add_button=True,
                on_add=lambda p=paper: add_paper(p),
                button_key=f"search_result_{idx}_{paper['id']}"
            )
elif st.session_state.last_search_query:
    st.info("No papers found matching your search.")