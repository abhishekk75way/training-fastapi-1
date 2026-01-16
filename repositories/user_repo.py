from sqlmodel import Session, select
from models.user import User

class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
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
    
    def update_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def delete_user(self, user: User) -> User:
        self.session.delete(user)
        self.session.commit()
        return user