import os
import uuid
from typing import Optional, List, BinaryIO
from datetime import datetime, UTC
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.document_repository import (
    DocumentRepository,
    get_document_repository,
)
from .pdf import PDFService
from ..storage import StorageInterface, get_storage
from ..models.document import ProcessingStatus, Document
from ..schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from ..core.logging import get_logger

logger = get_logger(__name__)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_MIME_TYPES = ["application/pdf"]


class DocumentService:
    def __init__(
        self,
        document_repo: Optional[DocumentRepository] = None,
        storage: Optional[StorageInterface] = None,
    ):
        self.document_repo = document_repo or get_document_repository()
        self.storage = storage or get_storage()

    def upload_document(
        self,
        db: Session,
        user_id: str,
        file: UploadFile,
    ) -> DocumentResponse:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)} MB",
            )
        # Validate MIME type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only PDFs are allowed.",
            )
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        # Save file to storage
        storage_path = self.storage.save_file(unique_filename, file.file)
        # Create document record in DB
        file_size = file.size or 0
        doc_create = DocumentCreate(
            user_id=user_id,
            filename=unique_filename,
            original_filename=file.filename or "unknown.pdf",
            file_size=file_size,
            mime_type=file.content_type or "application/pdf",
            storage_path=storage_path,
            processing_status=ProcessingStatus.UPLOADED,
        )
        doc = self.document_repo.create(db, doc_create.model_dump())
        logger.info(f"Document uploaded: {doc.id} by user {user_id}")
        return DocumentResponse.model_validate(doc)

    def process_document(
        self,
        db: Session,
        document_id: str,
        user_id: str,
    ) -> DocumentResponse:
        doc = self.document_repo.get_by_id_and_user(db, document_id, user_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        if doc.processing_status == ProcessingStatus.PROCESSING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document is already being processed",
            )
        # Update status to processing
        doc.processing_status = ProcessingStatus.PROCESSING
        db.commit()
        db.refresh(doc)

        try:
            # Extract text page-by-page
            pages = PDFService.extract_pages_from_pdf(doc.storage_path)
            extracted_text = "\n".join(p["text"] for p in pages)
            page_count = len(pages)
            word_count = len(extracted_text.split())
            character_count = len(extracted_text)

            # Chunk pages and prepare data
            chunks_to_create = []
            chunk_texts = []
            chunk_size = 1000
            overlap = 200

            for page in pages:
                page_num = page["page_number"]
                page_text = page["text"]

                if not page_text.strip():
                    continue

                if len(page_text) <= chunk_size:
                    page_chunks = [page_text]
                else:
                    page_chunks = []
                    start = 0
                    while start < len(page_text):
                        end = start + chunk_size
                        page_chunks.append(page_text[start:end])
                        start += chunk_size - overlap

                for chunk_content in page_chunks:
                    chunks_to_create.append({
                        "page_number": page_num,
                        "content": chunk_content
                    })
                    chunk_texts.append(chunk_content)

            # Generate embeddings and add chunks to DB session
            if chunk_texts:
                from ..ai.providers import get_ai_provider
                from ..models.document_chunk import DocumentChunk
                
                ai_provider = get_ai_provider()
                embeddings = ai_provider.get_embeddings(chunk_texts, task_type="retrieval_document")
                
                for i, chunk_data in enumerate(chunks_to_create):
                    db_chunk = DocumentChunk(
                        document_id=doc.id,
                        page_number=chunk_data["page_number"],
                        content=chunk_data["content"],
                        embedding=embeddings[i]
                    )
                    db.add(db_chunk)

            # Update document with results
            doc_update = DocumentUpdate(
                processing_status=ProcessingStatus.READY,
                extracted_text=extracted_text,
                page_count=page_count,
                word_count=word_count,
                character_count=character_count,
                processed_at=datetime.now(UTC),
            )
            for key, value in doc_update.model_dump(exclude_unset=True).items():
                setattr(doc, key, value)
            db.commit()
            db.refresh(doc)
            logger.info(f"Document processed successfully: {doc.id}")
        except Exception as e:
            logger.error(f"Failed to process document {doc.id}: {e}")
            doc.processing_status = ProcessingStatus.FAILED
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process document: {str(e)}",
            )
        return DocumentResponse.model_validate(doc)

    def get_user_documents(
        self,
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DocumentResponse]:
        docs = self.document_repo.get_by_user_id(db, user_id, skip, limit)
        return [DocumentResponse.model_validate(doc) for doc in docs]

    def get_document(
        self,
        db: Session,
        document_id: str,
        user_id: str,
    ) -> DocumentResponse:
        doc = self.document_repo.get_by_id_and_user(db, document_id, user_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        return DocumentResponse.model_validate(doc)

    def delete_document(
        self,
        db: Session,
        document_id: str,
        user_id: str,
    ) -> None:
        doc = self.document_repo.get_by_id_and_user(db, document_id, user_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )
        # Delete file from storage
        try:
            self.storage.delete_file(doc.storage_path)
        except Exception as e:
            logger.warning(f"Failed to delete file from storage: {e}")
        # Delete from DB
        db.delete(doc)
        db.commit()
        logger.info(f"Document deleted: {doc.id} by user {user_id}")

def get_document_service() -> DocumentService:
    return DocumentService()
