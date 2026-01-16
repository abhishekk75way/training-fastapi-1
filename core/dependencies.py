from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt 
from core.config import settings
from sqlmodel import Session
from db.session import get_session
from models.user import User, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")

        user = session.get(UserResponse, user_id)
        if not user:
            raise credentials_exception
        
        return user

    except JWTError:
        raise credentials_exception

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user