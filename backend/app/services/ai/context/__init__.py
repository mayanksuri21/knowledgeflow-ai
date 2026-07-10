from .document_provider import DocumentContextProvider, SimpleDocumentContextProvider


def get_document_context_provider() -> DocumentContextProvider:
    return SimpleDocumentContextProvider()
