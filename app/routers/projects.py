from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app import schemas, models, crud
from app.database import get_session
from app.dependencies import get_current_user
from app.utils import require_permission

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.get("/", response_model=list[schemas.ProjectRead])
async def read_projects(session: Session = Depends(get_session)):
    return crud.get_projects(session)

@router.post("/", response_model=schemas.ProjectRead)
@require_permission("create")
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    new_project = models.Project(
        name=project.name,
        description=project.description
    )
    return crud.create_project(session, new_project)

@router.put("/{project_id}", response_model=schemas.ProjectRead)
@require_permission("update")
async def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Retrieve the project
    db_projects = crud.get_projects(session)
    db_project = next((p for p in db_projects if p.id == project_id), None)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    db_project.name = project.name
    db_project.description = project.description
    return crud.update_project(session, db_project)

@router.delete("/{project_id}")
@require_permission("delete")
async def delete_project(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_projects = crud.get_projects(session)
    db_project = next((p for p in db_projects if p.id == project_id), None)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    crud.delete_project(session, db_project)
    return {"detail": "Project deleted"}