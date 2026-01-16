from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=50)
    email: str = Field(index=True, unique=True)
    password: str = Field(min_length=6)
    role: str = Field(default="user")

class UserResponse(SQLModel):
    name: str 
    email: str