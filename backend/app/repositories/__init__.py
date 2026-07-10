from .base import BaseRepository
from .user_repository import UserRepository
from .document_repository import DocumentRepository


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_document_repository() -> DocumentRepository:
    return DocumentRepository()
