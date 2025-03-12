from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app import models, schemas, crud
from app.database import get_session
from app.dependencies import get_current_user
from app.utils import require_permission

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/", response_model=list[schemas.DocumentRead])
async def read_documents(session: Session = Depends(get_session)):
    return crud.get_documents(session)

@router.post("/", response_model=schemas.DocumentRead)
@require_permission("create")
async def create_document(
    document: schemas.DocumentCreate,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    new_document = models.Document(
        title=document.title,
        content=document.content,
        owner_id=current_user.id
    )
    return crud.create_document(session, new_document)

@router.put("/{document_id}", response_model=schemas.DocumentRead)
@require_permission("update")
async def update_document(
    document_id: int,
    document: schemas.DocumentCreate,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    db_documents = crud.get_documents(session)
    db_document = next((d for d in db_documents if d.id == document_id), None)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    db_document.title = document.title
    db_document.content = document.content
    return crud.update_document(session, db_document)

@router.delete("/{document_id}")
@require_permission("delete")
async def delete_document(
    document_id: int,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_documents = crud.get_documents(session)
    db_document = next((d for d in db_documents if d.id == document_id), None)
    if not db_document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    crud.delete_document(session, db_document)
    return {"detail": "Document deleted"}