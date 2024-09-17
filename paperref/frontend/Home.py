import streamlit as st 
# configure page settings
st.set_page_config(
    page_title='Home',
    initial_sidebar_state='expanded')

import jwt
import extra_streamlit_components as stx
from authentication import authenticate_user, logout_user


# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")
    
# check if user is authenticated
authenticated = st.session_state.get('authenticated', False)
# if not authenticated, show login/register widget
if not authenticated:
    authenticate_user()
# otherwise show welcome page
else:
    # FIXME: not properly displaying the username right now
    username = st.session_state.username
    st.header('Welcome %s' % username)
    
    
with st.sidebar:
    if st.button('Logout'):
        logout_user()
