import streamlit as st
st.set_page_config(page_title='Recommended', page_icon='💡', layout='wide')

from src.api.auth import check_cookie
from src.api.library import get_recommendations_for_user


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")


# PAGE CONTENT

# header
st.markdown("### Recommended")
st.sidebar.header("Recommended")

# check authentication
check_cookie()
# if not authenticated, stop page rendering
if not st.session_state.get('authenticated', False):
    st.error("You must be logged in to view this page.")
    st.stop()
    
# fetch recommendations from backend
if st.session_state.get('recommended_papers', None) is None:
    st.session_state.recommended_papers = get_recommendations_for_user()
    
# display recommended papers
st.dataframe(
    st.session_state.recommended_papers, 
    column_config={
        'Title': st.column_config.TextColumn(width=450),
        'Authors': st.column_config.TextColumn(width=150),
        'Date': st.column_config.DateColumn("Date"),
        "URL": st.column_config.LinkColumn("URL", width=50),
    },
    hide_index=True,)