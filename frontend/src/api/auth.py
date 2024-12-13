"""
This module handles user authentication in a Streamlit application using Firebase for
login, registration, and session management.

The key functionalities provided by this module include:
- User login and registration via Firebase REST API.
- Secure handling of user credentials with session tokens.
- Management of authentication cookies using JWT for persistent login sessions.
- Streamlit user interface for login and registration.
"""

from datetime import datetime, timedelta
import json
import requests

import streamlit as st
import extra_streamlit_components as stx
import jwt


# Load cookie manager for handling user authentication cookies
cookie_manager = stx.CookieManager()


def login(email, password) -> bool:
    """
    Performs user login through the backend.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    url = f"{st.secrets['backend']['url']}/auth/login"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {"email": email, "password": password}
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            response = response.json()
            st.session_state.username = email
            st.session_state.id_token = response["id_token"]
            st.session_state.refresh_token = response["refresh_token"]
            expires_in = int(response["expires_in"])
            st.session_state.id_token_expiry = datetime.now() + timedelta(
                seconds=expires_in
            )
            return True
        else:
            error_message = response.json().get("detail", "An unknown error occurred.")
            st.error(error_message)
            return False
    except requests.exceptions.RequestException as error:
        message = json.loads(error.args[1])["error"]["message"]
        st.error(f"{message}")
        return False


def register(email, password) -> bool:
    """
    Signs up a new user through the backend.

    Args:
        email (str): The user's email address.
        password (str): The user's chosen password.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    url = f"{st.secrets['backend']['url']}/auth/register"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {"email": email, "password": password}
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            response = response.json()
            st.session_state.username = email
            st.session_state.id_token = response["id_token"]
            st.session_state.refresh_token = response["refresh_token"]
            expires_in = int(response["expires_in"])
            st.session_state.id_token_expiry = datetime.now() + timedelta(
                seconds=expires_in
            )
            return True
        else:
            error_message = response.json().get("detail", "An unknown error occurred.")
            st.error(error_message)
            return False
    except requests.exceptions.RequestException as error:
        message = json.loads(error.args[1])["error"]["message"]
        st.error(f"{message}")
        return False


def check_id_token() -> None:
    """Checks and refreshes the user id_token if it has expired."""
    expiry_time = st.session_state.get("id_token_expiry", None)
    if expiry_time and datetime.now() > expiry_time:
        refresh_id_token()


def refresh_id_token() -> None:
    """Refreshes the user id_token through the backend."""
    token = st.session_state.refresh_token
    url = f"{st.secrets['backend']['url']}/auth/refresh_token?refresh_token={token}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            st.session_state.id_token = response["id_token"]
            st.session_state.refresh_token = response["refresh_token"]
            expires_in = int(response["expires_in"])
            st.session_state.id_token_expiry = datetime.now() + timedelta(
                seconds=expires_in
            )
        else:
            error_message = response.json().get("detail", "An unknown error occurred.")
            st.error(error_message)
    except requests.exceptions.RequestException as error:
        message = json.loads(error.args[1])["error"]["message"]
        st.error(f"{message}")


def encode_cookie() -> str:
    """
    Encodes user authentication details into a JWT for storing in a cookie.

    Returns:
        str: Encoded JWT token.
    """
    cookie_dict = {
        "username": st.session_state.username,
        "id_token": st.session_state.id_token,
        "refresh_token": st.session_state.refresh_token,
        "id_token_expiry": st.session_state.id_token_expiry.isoformat(),
    }
    token = jwt.encode(cookie_dict, st.secrets["cookie"]["key"], algorithm="HS256")
    return token


def decode_cookie(token: str) -> dict:
    """
    Decodes a JWT token to retrieve user authentication details.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: Decoded token contents as a dictionary.
    """
    cookie_dict = jwt.decode(
        token, key=st.secrets["cookie"]["key"], algorithms=["HS256"]
    )
    return cookie_dict


def get_cookie() -> dict:
    """
    Retrieves the authentication cookie, if it exists and is valid.

    Returns:
        dict: The cookie's content if valid, otherwise None.
    """
    token = cookie_manager.get(st.secrets["cookie"]["name"])
    if token is not None:
        return decode_cookie(token)
    return None


def set_cookie() -> None:
    """
    Sets an authentication cookie with a valid token.
    """
    token = encode_cookie()
    exp_date = datetime.now() + timedelta(days=st.secrets["cookie"]["expiry_days"])
    cookie_manager.set(
        cookie=st.secrets["cookie"]["name"], val=token, expires_at=exp_date
    )


def delete_cookie() -> None:
    """
    Deletes the authentication cookie from the user's browser.
    """
    cookie_manager.delete(st.secrets["cookie"]["name"])


def authenticate_user():
    """
    Creates a user interface for login and registration, handling authentication.

    If the login or registration is successful, it sets an authentication cookie.
    """
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        st.header("Login")
        # Login form
        login_form = st.form(key="login")
        email = login_form.text_input("Email")
        password = login_form.text_input("Password", type="password")
        # On form submit, process login details
        if login_form.form_submit_button("Login"):
            if login(email, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()
    with register_tab:
        st.header("Register")
        # Register form
        register_form = st.form(key="register")
        email = register_form.text_input("Email")
        password = register_form.text_input("Password", type="password")
        confirm_password = register_form.text_input("Confirm Password", type="password")
        # On form submit, process registration details
        if register_form.form_submit_button("Register"):
            if password != confirm_password:
                st.error("Passwords must match")
            elif register(email, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()


def logout_user() -> None:
    """
    Logs out the authenticated user by clearing session state and deleting cookies.
    """
    if st.session_state.authenticated:
        delete_cookie()
        st.session_state.clear()
        st.rerun()


def check_cookie() -> None:
    """
    Checks if the user has a valid authentication cookie and sets session state accordingly.
    """
    cookie = get_cookie()
    if cookie:
        st.session_state.authenticated = True
        st.session_state.username = cookie["username"]
        st.session_state.id_token = cookie["id_token"]
        st.session_state.refresh_token = cookie["refresh_token"]
        st.session_state.id_token_expiry = datetime.fromisoformat(
            cookie["id_token_expiry"]
        )
