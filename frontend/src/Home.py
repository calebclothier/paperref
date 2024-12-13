import streamlit as st

st.set_page_config(page_title="Home", initial_sidebar_state="expanded")

from src.api.auth import authenticate_user, logout_user, check_cookie
# from src.utils import load_css


# # load custom styles
# load_css("styles/buttons.css")


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png",
)


# check cookies
check_cookie()
# if not authenticated, show login/register widget
if not st.session_state.get("authenticated", False):
    authenticate_user()
# otherwise show welcome page
else:
    st.header("Welcome")
    # logout widget sidebar
    with st.sidebar:
        if st.button("Logout"):
            logout_user()
