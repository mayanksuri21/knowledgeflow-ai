from .user_service import UserService
from .ai import get_ai_service, AIService
from .document_service import DocumentService, get_document_service


def get_user_service() -> UserService:
    return UserService()


def get_document_service() -> DocumentService:
    return DocumentService()