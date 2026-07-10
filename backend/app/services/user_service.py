from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..repositories.user_repository import UserRepository
from ..core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self, user_repo: Optional[UserRepository] = None):
        self.user_repo = user_repo or UserRepository()

    def get_or_create_user(
        self,
        db: Session,
        clerk_id: str,
        email: str,
        full_name: Optional[str] = None,
        profile_image: Optional[str] = None
    ) -> User:
        existing_user = self.user_repo.get_by_clerk_id(db, clerk_id=clerk_id)
        if existing_user:
            logger.info("User found", user_id=existing_user.id, clerk_id=clerk_id)
            return existing_user

        user_data = UserCreate(
            clerk_id=clerk_id,
            email=email,
            full_name=full_name,
            profile_image=profile_image
        )
        user = self.user_repo.create(db, obj_in=user_data.model_dump())
        logger.info("New user created", user_id=user.id, clerk_id=clerk_id)
        return user

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        return self.user_repo.get(db, id=user_id)

    def get_user_by_clerk_id(self, db: Session, clerk_id: str) -> Optional[User]:
        return self.user_repo.get_by_clerk_id(db, clerk_id=clerk_id)
