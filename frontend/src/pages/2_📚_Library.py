import streamlit as st

# NOTE: config must be before module-level imports
st.set_page_config(page_title="Paper Library", page_icon="📚", layout="wide")

from src.api.auth import check_cookie
from src.api.library import get_library, delete_paper
from src.components.paper_display import display_paper_sidebar
from src.utils.papers import format_title, get_first_author, get_last_author, get_best_link



# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png",
)


# header
st.markdown("### Your Library")

# check authentication
check_cookie()
# if not authenticated, stop page rendering
if not st.session_state.get("authenticated", False):
    st.error("You must be logged in to view this page.")
    st.stop()

# Get library from backend
if not st.session_state.get("library_loaded", False):
    papers_df = get_library()
    st.session_state["papers_df"] = papers_df
    st.session_state["library_loaded"] = True

# If library is empty, stop page rendering
if st.session_state["papers_df"] is None or st.session_state["papers_df"].empty:
    st.info("Your library is empty. Search for papers to add them to your library.")
    st.stop()

# Format rows
st.session_state["papers_df"]['title'] = st.session_state["papers_df"]['title'].apply(format_title)
st.session_state["papers_df"]['first_author'] = st.session_state["papers_df"]['authors'].apply(get_first_author)
st.session_state["papers_df"]['last_author'] = st.session_state["papers_df"]['authors'].apply(get_last_author)
st.session_state["papers_df"]['best_link'] = st.session_state["papers_df"].apply(get_best_link, axis=1)

# Display the dataframe with selection enabled
event = st.dataframe(
    st.session_state["papers_df"][["title", "first_author", "last_author", "journal", "citation_count", "publication_date"]],
    column_config={
        "title": st.column_config.TextColumn("Title", width="large"),
        "first_author": st.column_config.TextColumn("First Author", width="small"),
        "last_author": st.column_config.TextColumn("Last Author", width="small"),
        "journal": st.column_config.TextColumn("Journal", width="small"),
        "citation_count": st.column_config.NumberColumn("Citations", width="small"),
        "publication_date": st.column_config.DateColumn("Publication Date"),
    },
    hide_index=True,
    use_container_width=True,
    on_select="rerun",
    selection_mode="single-row",
)

# Update selected paper when a row is selected
if event.selection.rows:
    selected_idx = event.selection.rows[0]
    st.session_state.selected_paper = st.session_state["papers_df"].iloc[selected_idx].to_dict()

# If a paper is selected, display its details in the sidebar
if st.session_state.get("selected_paper", None):
    with st.sidebar:
        display_paper_sidebar(
            st.session_state.selected_paper,
            on_remove=lambda p=st.session_state.selected_paper: delete_paper(p['id']),
            button_key=f"selected_{st.session_state.selected_paper['id']}",
        )