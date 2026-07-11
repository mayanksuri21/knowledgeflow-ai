from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from ....repositories import DocumentRepository, get_document_repository


class DocumentContextProvider(ABC):
    @abstractmethod
    def get_context(self, db: Session, document_id: str) -> Optional[str]:
        pass


class SimpleDocumentContextProvider(DocumentContextProvider):
    def __init__(self, document_repo: Optional[DocumentRepository] = None):
        self.document_repo = document_repo or get_document_repository()

    def get_context(self, db: Session, document_id: str) -> Optional[str]:
        doc = self.document_repo.get(db, id=document_id)
        if doc and doc.extracted_text:
            return doc.extracted_text
        return None
