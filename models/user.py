from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="user")

class UserCreate(SQLModel):
    email: str
    password: str

class UserResponse(SQLModel):
    id: int
    email: str
    role: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    role: Optional[str] = None