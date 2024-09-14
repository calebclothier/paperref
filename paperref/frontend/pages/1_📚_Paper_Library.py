import streamlit as st
import pandas as pd


# configure page settings
st.set_page_config(
    page_title="Paper Library", 
    page_icon='📚',
    layout='wide')

# add logo to top left corner
st.logo(
    "assets/logo/large.png",
    link="https://paperref.com",
    icon_image="assets/logo/small.png")


# PAGE CONTENT

# header
st.markdown("## Paper Library")
st.sidebar.header("Paper Library")