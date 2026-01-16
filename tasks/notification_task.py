from db.session import SessionLocal
from repositories.notification_repo import NotificationRepo
from models.notification import Notification


def send_notification_task(
    sender_id: int,
    receiver_id: int,
    message: str,
):
    session = SessionLocal()
    try:
        repo = NotificationRepo(session)

        notification = Notification(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
        )

        repo.create(notification)

        print(f"[NOTIFICATION] {sender_id} → {receiver_id}: {message}")

    finally:
        session.close()
