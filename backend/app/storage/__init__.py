from .storage_interface import StorageInterface
from .local_storage import LocalStorage
from ..core.config import get_settings


def get_storage() -> StorageInterface:
    settings = get_settings()
    if settings.STORAGE_TYPE == "local":
        return LocalStorage()
    else:
        raise ValueError(f"Unsupported storage type: {settings.STORAGE_TYPE}")
