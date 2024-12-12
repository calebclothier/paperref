from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Authentication request class.
    
    Instance variables are an email str and a passowrd str
    """
    email: str
    password: str


class AuthResponse(BaseModel):
    """Authentication response class.
    
    Instance variables are initial id_token str, which is replaced by the 
    refresh_token str once the id_token expires after expires_in.
    """
    id_token: str
    refresh_token: str
    expires_in: str
    