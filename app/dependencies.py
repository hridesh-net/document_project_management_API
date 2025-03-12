from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from sqlmodel import Session, select
from app.models import User
from app.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        # Query the database for the complete user record (with role and permissions)
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )