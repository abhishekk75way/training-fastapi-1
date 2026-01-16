from fastapi import APIRouter

from .auth import router as auth_router
from .admin import router as admin_router
from .notifications import router as notifications_router

v2_router = APIRouter(prefix="/v2")

v2_router.include_router(auth_router)
v2_router.include_router(admin_router)
v2_router.include_router(notifications_router)

__all__ = ["v2_router"]