from .base import BaseRepository
from .user_repository import UserRepository


def get_user_repository() -> UserRepository:
    return UserRepository()
