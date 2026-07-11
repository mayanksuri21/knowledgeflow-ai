from .chat_service import ChatService, get_chat_service

def get_chat_service() -> ChatService:
    return ChatService()


__all__ = ["ChatService", "get_chat_service"]
