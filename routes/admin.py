from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_session
from services.auth_service import AdminService
from models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

def get_admin_service(session: Session = Depends(get_session)) -> AdminService:
    return AdminService(session)

@router.post("/register")
def register(user: User, admin_service: AdminService = Depends(get_admin_service)) -> User:
    return admin_service.register(user)

@router.get("/users")
def get_users(admin_service: AdminService = Depends(get_admin_service)) -> list[User]:
    return admin_service.get_users()

@router.get("/users/{user_id}")
def get_user(user_id: int, admin_service: AdminService = Depends(get_admin_service)) -> User:
    return admin_service.get_user(user_id)

@router.put("/users/{user_id}")
def update_user(user_id: int, user: User, admin_service: AdminService = Depends(get_admin_service)) -> User:
    return admin_service.update_user(user_id, user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, admin_service: AdminService = Depends(get_admin_service)) -> User:
    return admin_service.delete_user(user_id)