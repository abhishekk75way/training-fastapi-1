from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.session import get_session
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    return AuthService(session)

@router.post("/login")
def login(email: str, password: str, auth_service: AuthService = Depends(get_auth_service)) -> dict:
    token = auth_service.login(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(email: str, password: str, auth_service: AuthService = Depends(get_auth_service)) -> dict:
    user = auth_service.register(email, password)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully", "user": user}
