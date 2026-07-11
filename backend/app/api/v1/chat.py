from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ...models.user import User
from ...services.chat.chat_service import get_chat_service, ChatService
from ...schemas.chat import ChatQuestion, ChatAnswer
from ...core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/{document_id}", response_model=ChatAnswer, status_code=status.HTTP_200_OK)
async def chat_with_document(
    document_id: str,
    request: ChatQuestion,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service),
):
    """
    Endpoint to chat with a processed document.
    Verifies that the document exists, belongs to the current user,
    and has a processing status of 'ready'.
    """
    logger.info(
        "Chat request received",
        document_id=document_id,
        user_id=current_user.id,
        question=request.question,
    )
    try:
        result = chat_service.chat_with_document(
            db=db,
            document_id=document_id,
            user_id=current_user.id,
            question=request.question,
        )
        return result
    except HTTPException as e:
        # Re-raise FastAPI HTTP exceptions (e.g. 404, 400) from the service
        raise e
    except Exception as e:
        logger.error(
            "Unexpected error in chat endpoint",
            document_id=document_id,
            error=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during chat: {str(e)}",
        )
