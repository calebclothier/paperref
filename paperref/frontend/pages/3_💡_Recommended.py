import streamlit as st


# configure page settings
st.set_page_config(
    page_title='Recommended', 
    page_icon='💡',
    layout='wide')

# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")


# PAGE CONTENT

# header
st.markdown("## Recommended")
st.sidebar.header("Recommended")