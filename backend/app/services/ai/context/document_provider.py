from abc import ABC, abstractmethod
from typing import Optional


class DocumentContextProvider(ABC):
    @abstractmethod
    def get_context(self, document_id: str, query: Optional[str] = None) -> str:
        pass


class SimpleDocumentContextProvider(DocumentContextProvider):
    def get_context(self, document_id: str, query: Optional[str] = None) -> str:
        # In Version 1, we'll just return a placeholder
        # Later, this will extract and return document content
        return f"Document context for {document_id}"
