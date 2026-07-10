from typing import Optional
from .providers import AIProvider, get_ai_provider
from .context import DocumentContextProvider, get_document_context_provider
from .prompt_builder import PromptBuilder
from ...core.logging import get_logger

logger = get_logger(__name__)


class AIService:
    def __init__(
        self,
        ai_provider: Optional[AIProvider] = None,
        context_provider: Optional[DocumentContextProvider] = None,
        prompt_builder: Optional[PromptBuilder] = None
    ):
        self.ai_provider = ai_provider or get_ai_provider()
        self.context_provider = context_provider or get_document_context_provider()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def generate_response(self, query: str, document_id: str) -> str:
        logger.info("Generating AI response", document_id=document_id, query=query)
        context = self.context_provider.get_context(document_id, query)
        prompt = self.prompt_builder.build_prompt(query, context)
        response = self.ai_provider.generate_response(prompt, context)
        return response
