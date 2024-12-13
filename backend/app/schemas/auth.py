"""Classes to manage authentication requests and responses.
"""

from pydantic import BaseModel


class AuthRequest(BaseModel):
    """
    This class manages authentication requests, and inherits
    from pydantic's BaseModel.
    
    Attributes:
        email (str): the user's email address
        password (str): the user's password
    """
    email: str
    password: str


class AuthResponse(BaseModel):
    """
    This class manages authentication responses, and inherits
    from pydantic's BaseModel.
    
    Attributes:
        id_token (str): the user's ID token
        refresh_token (str): the user's refresh token which is still valid past expires_in
        expires_in (str): when the user's id_token expires
    """
    id_token: str
    refresh_token: str
    expires_in: str
