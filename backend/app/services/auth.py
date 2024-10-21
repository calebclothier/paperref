import requests

from fastapi import HTTPException

from app.config import settings


def login_service(email: str, password: str):
    """
    Performs user login through the Firebase REST API.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication
    """
    url = f"{settings.FIREBASE_AUTH_URL}signInWithPassword?key={settings.FIREBASE_API_KEY}"
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
                raise HTTPException(status_code=401, detail="Invalid email address.")
            elif error_message == "INVALID_LOGIN_CREDENTIALS":
                raise HTTPException(status_code=401, detail="Invalid login credentials.")
            elif error_message == "MISSING_PASSWORD":
                raise HTTPException(status_code=401, detail="Missing password.")
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                raise HTTPException(status_code=429, detail="Too many failed login attempts. Try again later.")
            else:
                raise HTTPException(status_code=400, detail=error_message)
        # Return valid auth response 
        response = response.json()
        return {
            'id_token': response['idToken'], 
            'refresh_token': response['refreshToken'], 
            'expires_in': response['expiresIn']}
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="An error occurred during authentication.")


def register_service(email: str, password: str):
    """
    Signs up a new user through the Firebase REST API.
    
    Args:
        email (str): The user's email address.
        password (str): The user's chosen password.

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication
    """
    url = f"{settings.FIREBASE_AUTH_URL}signUp?key={settings.FIREBASE_API_KEY}"
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
            if "EMAIL_EXISTS" in error_message:
                raise HTTPException(status_code=400, detail="Account already exists for provided email address.")
            elif "WEAK_PASSWORD" in error_message:
                raise HTTPException(status_code=400, detail="Weak password, must contain at least 6 characters.")
            elif "INVALID_EMAIL" in error_message:
                raise HTTPException(status_code=400, detail="Invalid email.")
            else:
                raise HTTPException(status_code=400, detail=error_message)
        # Return valid auth response 
        response = response.json()
        return {
            'id_token': response['idToken'], 
            'refresh_token': response['refreshToken'], 
            'expires_in': response['expiresIn']}
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="An error occurred during authentication.")


def refresh_id_token_service(refresh_token: str):
    """
    Generates a new id_token using a refresh_token through the Firebase REST API.
    
    Args:
        refresh_token (str): The user's refresh token

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication
    """
    url = f"https://securetoken.googleapis.com/v1/token?key={settings.FIREBASE_API_KEY}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    try:
        # Perform POST request to Firebase API for user login
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        # Handle non-200 response codes and display relevant error messages
        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', "An unknown error occurred.")
            raise HTTPException(status_code=response.status_code, detail=error_message)
        # Return valid auth response 
        response = response.json()
        return {
            'id_token': response['idToken'], 
            'refresh_token': response['refreshToken'], 
            'expires_in': response['expiresIn']}
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="An error occurred during authentication.")