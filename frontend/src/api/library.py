import requests

import pandas as pd
import streamlit as st

from src.api.auth import check_id_token


def load_library_for_user() -> pd.DataFrame:
    """
    Loads the user's paper library from the backend as a pandas `DataFrame`.

    This function sends a GET request to the backend to retrieve the user's paper library,
    processes the response, and returns a DataFrame with 'DOI' and 'Title' columns.
    It checks and refreshes the user's `id_token` before making the request.

    Returns:
        pd.DataFrame: A DataFrame containing the papers' DOIs and Titles, or an empty DataFrame if no papers are found.
    """
    # check and refresh id_token if necessary
    check_id_token()
    # backend GET request 
    url = f"{st.secrets['backend']['url']}/library/papers"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if not response:
                return pd.DataFrame(columns=['DOI', 'Title'])
            else:
                df = pd.DataFrame(response)
                df.columns = ['DOI', 'Title']
                return df
        else:
            st.error(response.json().get('detail', "Unable to load paper library."))
    except requests.exceptions.RequestException:
        st.error("Unable to load paper library.")
    return None


def save_library_for_user() -> None:
    """
    Saves the user's paper library to the backend.

    This function processes the user's paper library from the session state `DataFrame`
    into dictionary format, then sends a POST request to the backend to save it.
    It checks and refreshes the user's `id_token` before making the request.

    Returns:
        None
    """
    # check and refresh id_token if necessary
    check_id_token()
    # process from dataframe to dict
    papers_df = st.session_state.papers_df
    papers_df_renamed = papers_df.rename(columns={'DOI': 'doi', 'Title': 'title'})
    payload = papers_df_renamed.to_dict(orient='records')
    # backend POST request
    url = f"{st.secrets['backend']['url']}/library/papers"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}"}
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
        # TODO: error handling
    except requests.exceptions.RequestException:
        st.error("Unable to save paper library.")
    return None
    