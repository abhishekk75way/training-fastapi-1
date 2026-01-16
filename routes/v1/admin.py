from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db.session import get_session
from services.auth_service import AdminService
from models.user import UserCreate, UserResponse, UserUpdate
from core.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],  
)

def get_admin_service(
    session: Session = Depends(get_session),
) -> AdminService:
    return AdminService(session)


@router.get("/users", response_model=list[UserResponse])
def get_users(
    admin_service: AdminService = Depends(get_admin_service),
):
    return admin_service.get_all_users()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    user = admin_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    admin_service: AdminService = Depends(get_admin_service),
):
    user = admin_service.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin_service: AdminService = Depends(get_admin_service),
):
    if not admin_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.post("/register", response_model=UserResponse)
def register_admin(
    data: UserCreate,
    admin_service: AdminService = Depends(get_admin_service),
):
    try:
        return admin_service.create_admin(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))