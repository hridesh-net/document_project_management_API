# app/crud.py
from sqlmodel import Session, select
from app.models import User, Project, Document
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_username(session: Session, username: str) -> User:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    return results.first()

def create_project(session: Session, project: Project) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def update_project(session: Session, project: Project) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

def get_projects(session: Session):
    statement = select(Project)
    results = session.exec(statement)
    return results.all()

def create_document(session: Session, document: Document) -> Document:
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

def get_documents(session: Session):
    statement = select(Document)
    results = session.exec(statement)
    return results.all()

def update_document(session: Session, document: Document) -> Document:
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

def delete_document(session: Session, document: Document):
    session.delete(document)
    session.commit()