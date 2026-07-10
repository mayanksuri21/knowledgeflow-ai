from .user_service import UserService
from .document_service import DocumentService, get_document_service
from .ai import get_ai_service, AIService


def get_user_service() -> UserService:
    return UserService()
