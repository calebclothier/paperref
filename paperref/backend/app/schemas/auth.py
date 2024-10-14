from typing import Optional
from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Model for authentication requests."""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Model for authentication responses."""
    token: Optional[str] = None
    message: Optional[str] = None
    