from typing import Optional
from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    message: Optional[str] = None
    