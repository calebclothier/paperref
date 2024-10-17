import requests
import json

import pandas as pd
import streamlit as st


def load_library_for_user():
    url = f"{st.secrets['backend']['url']}/library/papers"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response = response.json()
        if not response:
            return pd.DataFrame(columns=['DOI', 'Title'])
        if isinstance(response, list):
            df = pd.DataFrame(response)
            df.columns = ['DOI', 'Title']
            return df
        if isinstance(response, dict):
            if response.get('detail', None):
                st.error(response['detail'])
    except requests.exceptions.HTTPError as error:
        message = json.loads(error.args[1])['error']['message']
        st.error(f'{message}')
    return None


def save_library_for_user():
    # process from dataframe to dict
    df = st.session_state.updated_df
    df_renamed = df.rename(columns={'DOI': 'doi', 'Title': 'title'})
    payload = df_renamed.to_dict(orient='records')
    # post request
    url = f"{st.secrets['backend']['url']}/library/papers"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}"
    }
    try:
        # Perform POST request to Firebase API for user login
        requests.post(url, headers=headers, json=payload, timeout=10)
        # TODO: error handling
    except requests.exceptions.HTTPError as error:
        message = json.loads(error.args[1])['error']['message']
        st.error(f'{message}')
    return None
    