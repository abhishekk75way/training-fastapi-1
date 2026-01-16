from models.user import User
from repositories.user_repo import UserRepo
from core.security import hash_password, verify_password, create_access_token
from sqlmodel import Session
from models.user import UserCreate

class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepo(session)

    def login(self, email: str, password: str) -> str | None:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return create_access_token(
            data={
                "sub": str(user.id),
                "role": user.role,
            }
        )

    def register(self, data: UserCreate) -> User:
        if self.user_repo.get_user_by_email(data.email):
            raise ValueError("User already exists")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )

        return self.user_repo.create_user(user)

class AdminService:
    def __init__(self, session: Session):
        self.user_repo = UserRepo(session)

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, data: UserUpdate):
        return self.user_repo.update_user(user_id, data)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete_user(user_id)
