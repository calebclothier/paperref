from fastapi import APIRouter
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth import login_service, register_service, refresh_id_token_service


router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(auth_request: AuthRequest) -> dict:
    """
    Login authentication of a user by email and password.

    Args:
        auth_request (AuthRequest): The request object containing user email and password.

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication.
    """
    return login_service(auth_request.email, auth_request.password)


@router.post("/register", response_model=AuthResponse)
def register(auth_request: AuthRequest) -> dict:
    """
    Registration authentication of a user by email and password.

    Args:
        auth_request (AuthRequest): The request object containing user email and password.

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication.
    """
    return register_service(auth_request.email, auth_request.password)


@router.post("/refresh_token", response_model=AuthResponse)
def refresh_id_token(refresh_token: str) -> dict:
    """
    Refresh token authentication of a user by email and password.

    Args:
        refresh_token (str): The user's refresh token

    Returns:
        dict: The auth tokens (id_token, refresh_token, expires_in)
        
    Raises:
        HTTPException: Any error that occurs during authentication.
    """
    return refresh_id_token_service(refresh_token)
