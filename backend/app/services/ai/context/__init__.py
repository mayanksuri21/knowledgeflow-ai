from .document_provider import DocumentContextProvider, RAGContextProvider


def get_document_context_provider() -> DocumentContextProvider:
    return RAGContextProvider()
