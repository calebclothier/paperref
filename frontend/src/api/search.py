"""Interface to backend REST API for searching papers."""

import requests
import streamlit as st

from src.api.auth import check_id_token


def search_papers(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """
    Searches for papers using the Semantic Scholar API via the backend.
    
    Args:
        query (str): The search query string
        limit (int): Maximum number of results to return (default: 5)
        
    Returns:
        list[dict]: The search results from the API
    """
    # check and refresh id_token if necessary
    check_id_token()
    
    # backend GET request
    url = f"{st.secrets['backend']['url']}/library/search"
    token = st.session_state.id_token
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params={
                "query": query.strip(),  # Ensure query is not None and strip whitespace
                "limit": limit
            },
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(response.json().get("detail", "Unable to search papers."))
    except requests.exceptions.RequestException:
        st.error("Unable to search papers.")
    return [] 