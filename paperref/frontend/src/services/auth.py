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


# Firebase auth URL
FIREBASE_AUTH_URL_BASE = "https://identitytoolkit.googleapis.com/v1/accounts:"

# Load cookie manager for handling user authentication cookies
cookie_manager = stx.CookieManager()


def login(email, password):
    """
    Performs user login through the Firebase REST API.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    url = f"{FIREBASE_AUTH_URL_BASE}signInWithPassword?key={st.secrets['firebase_web_api_key']}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True}
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        # Handle non-200 response codes and display relevant error messages
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', "An unknown error occurred.")
            if error_message == 'INVALID_EMAIL':
                st.error('Invalid email address.')
            elif error_message == "INVALID_LOGIN_CREDENTIALS":
                st.error('Invalid login credentials.')
            elif error_message == "MISSING_PASSWORD":
                st.error('Missing password.')
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                st.error("Access to this account has been temporarily disabled due to many failed login attempts.")
            else:
                st.error(f"{error_message}")
            return False
        # If login successful, store the email in session state
        response = response.json()
        if "idToken" in response:
            st.session_state.username = email
            return True
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        st.error(f'{error_message}')
    return False


def register(email, password):
    """
    Signs up a new user through the Firebase REST API.

    Args:
        email (str): The user's email address.
        password (str): The user's chosen password.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    url = f"{FIREBASE_AUTH_URL_BASE}signUp?key={st.secrets['firebase_web_api_key']}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True}
    try:
        # Perform POST request to Firebase API for user registration
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        # Handle non-200 response codes and display relevant error messages
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', 'An unknown error occurred.')
            if "EMAIL_EXISTS" in error_message:
                st.error("Account already exists for provided email address.")
            elif "WEAK_PASSWORD" in error_message:
                st.error("Weak password, must contain at least 6 characters.")
            elif "INVALID_EMAIL" in error_message:
                st.error("Invalid email.")
            else:
                st.error(f"{error_message}")
            return False
        # If registration successful, store the email in session state
        response = response.json()
        if "idToken" in response:
            st.session_state.username = email
            return True
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        st.error(f'{error_message}')
    return False


def encode_cookie():
    """
    Encodes user authentication details into a JWT for storing in a cookie.

    Returns:
        str: Encoded JWT token.
    """
    exp_date = (datetime.now() + timedelta(days=st.secrets["cookie"]["expiry_days"])).timestamp()
    cookie_dict = {
        'username': st.session_state.username,
        'exp_date': exp_date}
    token = jwt.encode(
        cookie_dict,
        st.secrets["cookie"]["key"],
        algorithm='HS256')
    return token


def decode_cookie(token):
    """
    Decodes a JWT token to retrieve user authentication details.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: Decoded token contents as a dictionary.
    """
    cookie_dict = jwt.decode(token, st.secrets["cookie"]["key"], algorithms=['HS256'])
    return cookie_dict


def get_cookie():
    """
    Retrieves the authentication cookie, if it exists and is valid.

    Returns:
        dict: The cookie's content if valid, otherwise None.
    """
    token = cookie_manager.get(st.secrets["cookie"]["name"])
    if token is not None:
        cookie_dict = decode_cookie(token)
        if (cookie_dict is not False and 'username' in cookie_dict and
            cookie_dict['exp_date'] > datetime.now().timestamp()):
            return cookie_dict
    return None


def set_cookie():
    """
    Sets an authentication cookie with a valid token.
    """
    token = encode_cookie()
    exp_date = datetime.now() + timedelta(days=st.secrets["cookie"]["expiry_days"])
    cookie_manager.set(st.secrets["cookie"]["name"], token, expires_at=exp_date)


def delete_cookie():
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
        login_form = st.form(key='login')
        email = login_form.text_input('Email')
        password = login_form.text_input('Password', type='password')
        # On form submit, process login details
        if login_form.form_submit_button('Login'):
            if login(email, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()

    with register_tab:
        st.header("Register")
        # Register form
        register_form = st.form(key='register')
        email = register_form.text_input('Email')
        password = register_form.text_input('Password', type='password')
        confirm_password = register_form.text_input('Confirm Password', type='password')
        # On form submit, process registration details
        if register_form.form_submit_button('Register'):
            if password != confirm_password:
                st.error('Passwords must match')
            elif register(email, password):
                set_cookie()
                st.session_state.authenticated = True
                st.rerun()


def logout_user():
    """
    Logs out the authenticated user by clearing session state and deleting cookies.
    """
    if st.session_state.authenticated:
        delete_cookie()
        st.session_state.clear()
        st.rerun()


def check_cookie():
    """
    Checks if the user has a valid authentication cookie and sets session state accordingly.
    """
    token = get_cookie()
    if token:
        st.session_state.authenticated = True
        st.session_state.username = token['username']
