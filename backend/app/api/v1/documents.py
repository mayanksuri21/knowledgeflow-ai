from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ...core.logging import get_logger
from ...models.user import User
from ...services import get_document_service, DocumentService
from ...schemas.document import DocumentResponse

router = APIRouter()
logger = get_logger(__name__)


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.upload_document(db, current_user.id, file)


@router.post("/{document_id}/process", response_model=DocumentResponse)
async def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.process_document(db, document_id, current_user.id)


@router.get("", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.get_user_documents(db, current_user.id, skip, limit)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service),
):
    return document_service.get_document(db, document_id, current_user.id)


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service),
):
    document_service.delete_document(db, document_id, current_user.id)
