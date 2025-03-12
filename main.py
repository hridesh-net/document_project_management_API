# app/main.py
from fastapi import FastAPI
from app.routers import auth, projects, documents
from app.database import init_db


init_db()

app = FastAPI(title="Backend API with JWT & RBAC")


app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)