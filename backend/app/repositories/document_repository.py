from typing import List, Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.document import Document


class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)

    def get_by_user_id(
        self,
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        return (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id_and_user(
        self,
        db: Session,
        document_id: str,
        user_id: str,
    ) -> Optional[Document]:
        return (
            db.query(Document)
            .filter(Document.id == document_id, Document.user_id == user_id)
            .first()
        )
