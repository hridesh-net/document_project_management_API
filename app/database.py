# app/database.py
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/dbname")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    import app.models
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session