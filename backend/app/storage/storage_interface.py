from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageInterface(ABC):
    @abstractmethod
    def save_file(self, file_name: str, file_content: BinaryIO) -> str:
        pass

    @abstractmethod
    def get_file(self, file_path: str) -> BinaryIO:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass
