from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from models.user import User
from core.dependencies import require_admin, get_current_user
from db.session import get_session
from tasks.notification_task import send_notification_task
from repositories.notification_repo import NotificationRepo

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

class NotificationRequest(BaseModel):
    receiver_id: int
    message: str

@router.post("/send")
def send_notification(
    receiver_id: int,
    message: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_admin),
):
    if receiver_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid receiver")

    background_tasks.add_task(
        send_notification_task,
        sender_id=current_user.id,
        receiver_id=receiver_id,
        message=message,
    )

    return {"message": "Notification queued"}

@router.get("/")
def get_notifications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    repo = NotificationRepo(session)
    return repo.get_for_user(current_user.id)

@router.post("/{notification_id}/read")
def read_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    repo = NotificationRepo(session)
    notification = repo.get_by_id(notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    if notification.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to read this notification")
        
    return repo.mark_as_read(notification)

