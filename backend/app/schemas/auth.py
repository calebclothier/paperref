from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Model for authentication requests."""
    email: str
    password: str


class AuthResponse(BaseModel):
<<<<<<< HEAD:paperref/backend/app/schemas/auth.py
    """Model for authentication responses."""
    token: Optional[str] = None
    message: Optional[str] = None
    
=======
    id_token: str
    refresh_token: str
    expires_in: str
>>>>>>> main:backend/app/schemas/auth.py
