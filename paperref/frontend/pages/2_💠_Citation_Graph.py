import streamlit as st
# configure page settings
st.set_page_config(
    page_title="Citation Graph",
    page_icon='💠',
    layout='wide')
from authentication import check_cookie


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")


# PAGE CONTENT

# header
st.markdown("## Citation Graph")
st.sidebar.header("Citation Graph")

# check authentication
check_cookie()
if not st.session_state.get('authenticated', False):
    st.error("You must be logged in to view this page.")
    st.stop()