import streamlit as st
st.set_page_config(page_title="Paper Library", page_icon='📚', layout='wide')

from src.api.auth import check_cookie
from src.api.library import load_library_for_user, save_library_for_user
# from src.utils import load_css


# # load custom styles
# load_css("styles/buttons.css")


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")


# header
st.markdown("### Paper Library")
st.sidebar.header("Paper Library")


# check authentication
check_cookie()
# if not authenticated, stop page rendering
if not st.session_state.get('authenticated', False):
    st.error("You must be logged in to view this page.")
    st.stop()


# data table
papers_df = load_library_for_user()
st.session_state.papers_df = st.data_editor(
    papers_df,
    use_container_width=True,
    column_config={
        'Title': st.column_config.TextColumn(width=600),
        'DOI': st.column_config.TextColumn(required=True, width=175)},
    hide_index=True,
    num_rows='dynamic')


# save button
b = st.button('Save', icon=":material/save:", on_click=save_library_for_user)
