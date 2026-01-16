from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from db.session import get_session
from services.auth_service import AuthService
from models.user import User, UserCreate
from core.dependencies import get_current_user
from repositories.notification_repo import NotificationRepo

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    return AuthService(session)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer",
    }


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

@router.get("/me")
def my_notifications(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    repo = NotificationRepo(session)
    return repo.get_for_user(current_user.id)
