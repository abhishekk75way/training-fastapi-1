from sqlmodel import Session
from models.notification import Notification


class NotificationRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, notification: Notification):
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification

    def get_for_user(self, user_id: int):
        return self.session.query(Notification)\
            .filter(Notification.receiver_id == user_id)\
            .order_by(Notification.created_at.desc())\
            .all()

    def get_by_id(self, notification_id: int):
        return self.session.query(Notification).filter(Notification.id == notification_id).first()

    def mark_as_read(self, notification: Notification):
        notification.is_read = True
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification
