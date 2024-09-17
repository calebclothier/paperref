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

# mock data
test_data = [
    [
        '10.1103/PhysRevX.12.021028',
        'Universal gate operations on nuclear spin qubits in an optical tweezer array of 171Yb atoms', 
    ], 
    [
        '10.1038/s41467-022-32094-6', 
        'Erasure conversion for fault-tolerant quantum computing in alkaline earth Rydberg atom arrays', 
    ],
    [        
        '10.1038/s41586-023-06438-1', 
        'High-fidelity gates with mid-circuit erasure conversion in a metastable neutral atom qubit', 
    ]
]
df = pd.DataFrame(test_data, columns=['DOI', 'Title'])

# data table
st.data_editor(
    df, 
    use_container_width=True,
    column_config={
        'Title': st.column_config.TextColumn(width=600),
        'DOI': st.column_config.TextColumn(required=True, width=175)},
    hide_index=True, 
    num_rows='dynamic')