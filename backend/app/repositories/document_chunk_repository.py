from typing import List
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.document_chunk import DocumentChunk


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    def __init__(self):
        super().__init__(DocumentChunk)

    def get_by_document_id(self, db: Session, document_id: str) -> List[DocumentChunk]:
        return (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.page_number, DocumentChunk.id)
            .all()
        )

    def create_multi(self, db: Session, objs_in: List[dict]) -> List[DocumentChunk]:
        db_objs = [self.model(**obj) for obj in objs_in]
        db.add_all(db_objs)
        db.commit()
        return db_objs

def get_document_chunk_repository() -> DocumentChunkRepository:
    return DocumentChunkRepository()