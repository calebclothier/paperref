from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: str