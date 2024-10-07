import requests
import json

from app.config import settings


def login_service(email: str, password: str):
    """
    Performs user login through the Firebase REST API.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: The login token and any error messages
    """
    url = f"{settings.FIREBASE_AUTH_URL}signInWithPassword?key={settings.FIREBASE_API_KEY}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True}
    token = None
    message = None
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        # Handle non-200 response codes and display relevant error messages
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', "An unknown error occurred.")
            if error_message == 'INVALID_EMAIL':
                message = 'Invalid email address.'
            elif error_message == "INVALID_LOGIN_CREDENTIALS":
                message = 'Invalid login credentials.'
            elif error_message == "MISSING_PASSWORD":
                message = 'Missing password.'
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                message = "Access to this account has been temporarily disabled due to many failed login attempts."
            else:
                message = f"{error_message}"
        # get idToken if it exists
        response = response.json()
        token = response.get('idToken', None)
    except requests.exceptions.HTTPError as error:
        message = json.loads(error.args[1])['error']['message']
    # return auth response
    return {'token': token, 'message': message}


def register_service(email: str, password: str):
    """
    Signs up a new user through the Firebase REST API.
    
    Args:
        email (str): The user's email address.
        password (str): The user's chosen password.

    Returns:
        dict: The login token and any error messages
    """
    url = f"{settings.FIREBASE_AUTH_URL}signUp?key={settings.FIREBASE_API_KEY}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True}
    token = None
    message = None
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        # Handle non-200 response codes and display relevant error messages
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', "An unknown error occurred.")
            if "EMAIL_EXISTS" in error_message:
                message = "Account already exists for provided email address."
            elif "WEAK_PASSWORD" in error_message:
                message = "Weak password, must contain at least 6 characters."
            elif "INVALID_EMAIL" in error_message:
                message = "Invalid email."
            else:
                message = f"{error_message}"
        # get idToken if it exists
        response = response.json()
        token = response.get('idToken', None)
    except requests.exceptions.HTTPError as error:
        message = json.loads(error.args[1])['error']['message']
    # return auth response
    return {'token': token, 'message': message}