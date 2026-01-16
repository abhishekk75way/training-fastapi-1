from models.user import User
from repositories.user_repo import UserRepo
from core.security import hash_password, verify_password, create_access_token
from sqlmodel import Session

class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepo(session)
    
    def login(self, email: str, password: str) -> str | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return create_access_token(data={"sub": user.email})
    
    def register(self, email: str, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if user:
            raise ValueError("User already exists")
        hashed_password = hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        return self.user_repo.create_user(user)

class AdminService:
    def __init__(self, session: Session):
        self.user_repo = UserRepo(session)
    
    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all_users()

__all__ = [
    "AuthService",
    "AdminService",
]
