from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from ....repositories import DocumentRepository, get_document_repository, DocumentChunkRepository, get_document_chunk_repository
from ..providers import get_ai_provider, AIProvider


class DocumentContextProvider(ABC):
    @abstractmethod
    def get_context(
        self, db: Session, document_id: str, query: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        pass


class SimpleDocumentContextProvider(DocumentContextProvider):
    def __init__(self, document_repo: Optional[DocumentRepository] = None):
        self.document_repo = document_repo or get_document_repository()

    def get_context(
        self, db: Session, document_id: str, query: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        doc = self.document_repo.get(db, id=document_id)
        if doc and doc.extracted_text:
            return doc.extracted_text, []
        return "", []


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot_product / (norm_a * norm_b)


class RAGContextProvider(DocumentContextProvider):
    def __init__(
        self,
        chunk_repo: Optional[DocumentChunkRepository] = None,
        ai_provider: Optional[AIProvider] = None,
    ):
        self.chunk_repo = chunk_repo or get_document_chunk_repository()
        self.ai_provider = ai_provider or get_ai_provider()

    def get_context(
        self, db: Session, document_id: str, query: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        if not query:
            return "", []

        # 1. Retrieve chunks
        chunks = self.chunk_repo.get_by_document_id(db, document_id)
        if not chunks:
            return "", []

        # 2. Embed query
        query_embeddings = self.ai_provider.get_embeddings([query], task_type="retrieval_query")
        if not query_embeddings:
            return "", []
        query_embedding = query_embeddings[0]

        # 3. Calculate similarities
        chunk_similarities = []
        for chunk in chunks:
            sim = cosine_similarity(query_embedding, chunk.embedding)
            chunk_similarities.append((sim, chunk))

        # 4. Sort by similarity descending and get top-5
        chunk_similarities.sort(key=lambda x: x[0], reverse=True)
        top_k = chunk_similarities[:5]

        # 5. Format context and extract citations
        context_parts = []
        citations = []
        for sim, chunk in top_k:
            context_parts.append(f"[Page {chunk.page_number}]: {chunk.content}")
            citations.append({
                "page_number": chunk.page_number,
                "content": chunk.content,
            })

        context_text = "\n\n".join(context_parts)
        return context_text, citations
