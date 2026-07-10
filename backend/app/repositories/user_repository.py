from typing import Optional
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_clerk_id(self, db: Session, clerk_id: str) -> Optional[User]:
        return db.query(User).filter(User.clerk_id == clerk_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
