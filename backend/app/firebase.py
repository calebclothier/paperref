""" Firebase verification module for authenticating backend requests
"""
import json

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import firebase_admin
from firebase_admin import credentials, auth

from app.config import settings


# Initialize the default app
cred = credentials.Certificate(json.loads(settings.FIREBASE_ADMIN_SDK_KEY))
firebase_app = firebase_admin.initialize_app(cred)


auth_scheme = HTTPBearer()

async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> str:
    """
    Verify the authorization id_token and extract the user_id (uid).
    
    Args:
        authorization (HTTPAuthorizationCredentials): the authorization credentials
        
    Returns:
        str: the user's id
        
    Raises:
        HTTPException: Raises Invalid or expired token
    """
    try:
        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(authorization.credentials)
        # Extract the uid (user_id)
        user_id = decoded_token["uid"]
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
