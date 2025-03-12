from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app import schemas, models, crud
from app.database import get_session
from jose import jwt
import os
from datetime import datetime, timedelta

router = APIRouter(tags=["authentication"])

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register")
def register(user: schemas.UserCreate, session: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    role_obj = session.exec(select(models.Role).where(models.Role.name == user.role)).first()
    if not role_obj:
        raise HTTPException(status_code=400, detail="Invalid role")
    hashed_password = crud.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role_id=role_obj.id
    )
    crud.create_user(session, new_user)
    return {"username": new_user.username, "role": role_obj.name}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, session: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(session, user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    role_name = db_user.role.name if db_user.role else "user"
    payload = {
        "user_id": db_user.id,
        "role": role_name,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}