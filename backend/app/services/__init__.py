from .user_service import UserService
from .ai import get_ai_service, AIService


def get_user_service() -> UserService:
    return UserService()
