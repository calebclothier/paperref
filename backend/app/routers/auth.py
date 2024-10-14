from fastapi import APIRouter
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth import login_service, register_service


router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(auth_request: AuthRequest):
    return login_service(auth_request.email, auth_request.password)


@router.post("/register", response_model=AuthResponse)
def register(auth_request: AuthRequest):
    return register_service(auth_request.email, auth_request.password)