from typing import Optional
from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    success: bool
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None
    error_message: Optional[str] = None