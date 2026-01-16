from models import UserUpdate
from sqlmodel import Session, select
from models.user import User, UserUpdate
from fastapi import HTTPException

class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement)
        return result.first()

    def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = self.session.exec(statement)
        return result.first()

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_all_users(self) -> list[User]:
        statement = select(User)
        result = self.session.exec(statement)
        return result.all()
    
    def update_user(self, user_id: int, user: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.email = user.email
        user.role = user.role
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete_user(self, user: User) -> User:
        self.session.delete(user)
        self.session.commit()
        return user