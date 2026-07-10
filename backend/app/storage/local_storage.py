import os
from typing import BinaryIO
from .storage_interface import StorageInterface
from ..core.config import get_settings
from ..core.logging import get_logger

logger = get_logger(__name__)


class LocalStorage(StorageInterface):
    def __init__(self):
        settings = get_settings()
        self.storage_path = settings.LOCAL_STORAGE_PATH
        os.makedirs(self.storage_path, exist_ok=True)

    def save_file(self, file_name: str, file_content: BinaryIO) -> str:
        file_path = os.path.join(self.storage_path, file_name)
        with open(file_path, "wb") as f:
            f.write(file_content.read())
        logger.info("File saved locally", file_path=file_path)
        return file_path

    def get_file(self, file_path: str) -> BinaryIO:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return open(file_path, "rb")

    def delete_file(self, file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("File deleted locally", file_path=file_path)
