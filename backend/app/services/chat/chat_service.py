from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..ai import get_ai_service, AIService
from ..document_service import get_document_service, DocumentService
from ...core.logging import get_logger
from ...models.document import ProcessingStatus

logger = get_logger(__name__)


class ChatService:
    def __init__(
        self,
        ai_service: AIService = None,
        document_service: DocumentService = None
    ):
        self.ai_service = ai_service or get_ai_service()
        self.document_service = document_service or get_document_service()

    def chat_with_document(
        self,
        db: Session,
        document_id: str,
        user_id: str,
        question: str
    ) -> Dict[str, Any]:
        if not question or not question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )

        # Get document and verify ownership
        doc_response = self.document_service.get_document(db, document_id, user_id)
        if not doc_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Check processing status
        if doc_response.processing_status != ProcessingStatus.READY.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document is not ready for chat. Current status: {doc_response.processing_status}"
            )

        # Generate response using AI service
        ai_response = self.ai_service.generate_response(db, question, document_id)

        return {
            "answer": ai_response["answer"],
            "document_id": document_id,
            "usage": ai_response["usage"],
            "citations": ai_response.get("citations", [])
        }


def get_chat_service() -> ChatService:
    return ChatService()
