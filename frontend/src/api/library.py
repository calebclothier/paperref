"""Interface to backend REST API for loading and saving user paper library."""

import requests

import pandas as pd
import streamlit as st

from src.api.auth import check_id_token


def get_library() -> pd.DataFrame:
    """
    Loads the user's paper library from the backend as a pandas `DataFrame`.

    This function sends a GET request to the backend to retrieve the user's paper library,
    processes the response, and returns a DataFrame with paper details.
    It checks and refreshes the user's `id_token` before making the request.

    Returns:
        pd.DataFrame: A DataFrame containing the papers' details, or an empty DataFrame if no papers are found.
    """
    # check and refresh id_token if necessary
    check_id_token()
    # backend GET request
    url = f"{st.secrets['backend']['url']}/library/papers"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if not response:
                return None
                # return pd.DataFrame(columns=["id", "title", "doi", "authors", "year", "journal"])
            else:
                df = pd.DataFrame(response)
                return df
        else:
            st.error(response.json().get("detail", "Unable to load paper library."))
    except requests.exceptions.RequestException:
        st.error("Unable to load paper library.")
    return None


def add_paper(paper: dict) -> bool:
    """
    Adds a single paper to the user's library.

    Args:
        paper (dict): The paper data to add to the library

    Returns:
        bool: True if the paper was successfully added, False otherwise
    """
    # check and refresh id_token if necessary
    check_id_token()
    # backend POST request
    url = f"{st.secrets['backend']['url']}/library/papers/add"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.post(url, headers=headers, json=paper, timeout=10)
        print(response.json())
        if response.status_code == 200:
            return True
        else:
            st.error(response.json().get("detail", "Unable to add paper to library."))
    except requests.exceptions.RequestException:
        st.error("Unable to add paper to library.")
    return False


def delete_paper(paper_id: str) -> bool:
    """
    Deletes a single paper from the user's library.

    Args:
        paper_id (str): The ID of the paper to delete

    Returns:
        bool: True if the paper was successfully deleted, False otherwise
    """
    # check and refresh id_token if necessary
    check_id_token()
    # backend DELETE request
    url = f"{st.secrets['backend']['url']}/library/papers/{paper_id}"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.delete(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return True
        else:
            st.error(response.json().get("detail", "Unable to delete paper from library."))
    except requests.exceptions.RequestException:
        st.error("Unable to delete paper from library.")
    return False


def get_recommendations() -> list[dict] | None:
    """
    Fetches paper recommendations for the user.

    Returns:
        pd.DataFrame: A DataFrame containing recommended papers, or None if the request fails.
    """
    # check and refresh id_token if necessary
    check_id_token()
    # backend GET request
    url = f"{st.secrets['backend']['url']}/recommended"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.get(url, headers=headers, timeout=120)
        if response.status_code == 200:
            response = response.json()
            df = pd.DataFrame(
                response,
                columns=[
                    "title",
                    "authors",
                    "publication_date",
                    "citation_count",
                    "open_access_url",
                ],
            )
            df["authors"] = df["authors"].apply(lambda x: ", ".join(x))
            df["publication_date"] = pd.to_datetime(df["publication_date"])
            df.columns = ["Title", "Authors", "Date", "Citations", "URL"]
            return df
        else:
            st.error(response.json().get("detail", "Unable to fetch recommendations."))
    except requests.exceptions.RequestException:
        st.error("Unable to fetch recommendations.")
    return None
