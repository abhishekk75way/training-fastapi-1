from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.session import get_session
from services.auth_service import AuthService
from models.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    return AuthService(session)

@router.post("/login")
def login(
    data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    token = auth_service.login(data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(
    data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = auth_service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": "User registered successfully",
        "user": user,
    }
