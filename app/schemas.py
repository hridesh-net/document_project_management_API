# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True