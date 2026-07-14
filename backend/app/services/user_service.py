from typing import Optional
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate
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
        """
        Get an existing user or create one if it doesn't exist.

        Flow:
        1. Find by Clerk ID.
        2. If not found, find by email.
        3. If email exists, update the Clerk ID and profile.
        4. Otherwise create a new user.
        """

        # Step 1: Find by Clerk ID
        existing_user = self.user_repo.get_by_clerk_id(
            db,
            clerk_id=clerk_id
        )

        if existing_user:
            logger.info(
                "User found by Clerk ID",
                user_id=existing_user.id,
                clerk_id=clerk_id
            )
            return existing_user

        # Step 2: Find by email
        existing_user = self.user_repo.get_by_email(
            db,
            email=email
        )

        if existing_user:
            existing_user.clerk_id = clerk_id
            existing_user.full_name = full_name
            existing_user.profile_image = profile_image

            db.commit()
            db.refresh(existing_user)

            logger.info(
                "Existing user linked with new Clerk ID",
                user_id=existing_user.id,
                clerk_id=clerk_id
            )

            return existing_user

        # Step 3: Create a brand-new user
        user_data = UserCreate(
            clerk_id=clerk_id,
            email=email,
            full_name=full_name,
            profile_image=profile_image
        )

        user = self.user_repo.create(
            db,
            obj_in=user_data.model_dump()
        )

        logger.info(
            "New user created",
            user_id=user.id,
            clerk_id=clerk_id
        )

        return user

    def get_user_by_id(
        self,
        db: Session,
        user_id: str
    ) -> Optional[User]:
        return self.user_repo.get(db, id=user_id)

    def get_user_by_clerk_id(
        self,
        db: Session,
        clerk_id: str
    ) -> Optional[User]:
        return self.user_repo.get_by_clerk_id(db, clerk_id=clerk_id)