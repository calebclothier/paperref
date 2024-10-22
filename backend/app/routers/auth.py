from fastapi import APIRouter
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth import (
    login_service, 
    register_service, 
    refresh_id_token_service)


router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(auth_request: AuthRequest):
    return login_service(auth_request.email, auth_request.password)


@router.post("/register", response_model=AuthResponse)
def register(auth_request: AuthRequest):
    return register_service(auth_request.email, auth_request.password)


@router.post("/refresh_token", response_model=AuthResponse)
def refresh_id_token(refresh_token: str):
    return refresh_id_token_service(refresh_token)