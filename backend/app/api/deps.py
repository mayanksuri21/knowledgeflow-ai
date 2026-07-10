from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import clerk_auth, security, HTTPAuthorizationCredentials
from ..models.user import User
from ..repositories.user_repository import UserRepository, get_user_repository
from ..schemas.user import UserResponse
from ..core.logging import get_logger

logger = get_logger(__name__)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    token = credentials.credentials
    payload = clerk_auth.verify_token(token)
    clerk_id = payload.get("sub")
    if not clerk_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = user_repo.get_by_clerk_id(db, clerk_id=clerk_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info("User authenticated", user_id=user.id, clerk_id=clerk_id)
    return user
