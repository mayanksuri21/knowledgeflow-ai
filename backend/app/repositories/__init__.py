from .base import BaseRepository
from .user_repository import UserRepository
from .document_repository import DocumentRepository
from .document_chunk_repository import DocumentChunkRepository


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_document_repository() -> DocumentRepository:
    return DocumentRepository()


def get_document_chunk_repository() -> DocumentChunkRepository:
    return DocumentChunkRepository()
