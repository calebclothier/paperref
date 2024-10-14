from typing import Optional
from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Model for an authentication request."""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Model for an authentication response."""
    token: Optional[str] = None
    message: Optional[str] = None
    