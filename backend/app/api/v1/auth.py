from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..deps import get_db, get_current_user
from ...core.logging import get_logger
from ...services import UserService, get_user_service
from ...schemas.user import UserResponse
from ...models.user import User

logger = get_logger(__name__)
router = APIRouter()


class SyncUserRequest(BaseModel):
    clerk_id: str
    email: EmailStr
    full_name: Optional[str] = None
    profile_image: Optional[str] = None


@router.post("/sync-user", response_model=UserResponse)
async def sync_user(
    request: SyncUserRequest,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_or_create_user(
        db,
        clerk_id=request.clerk_id,
        email=request.email,
        full_name=request.full_name,
        profile_image=request.profile_image
    )
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
