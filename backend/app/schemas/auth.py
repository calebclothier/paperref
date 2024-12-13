from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Model for authentication requests."""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Model for authentication responses."""
    id_token: str
    refresh_token: str
    expires_in: str
