from abc import ABC, abstractmethod
from typing import Dict, Any
import google.generativeai as genai
from ....core.config import get_settings
from ....core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_embeddings(self, texts: list[str], task_type: str = "retrieval_document") -> list[list[float]]:
        pass


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def get_embeddings(self, texts: list[str], task_type: str = "retrieval_document") -> list[list[float]]:
        if not texts:
            return []
        try:
            batch_size = 100
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=batch,
                    task_type=task_type
                )
                all_embeddings.extend(result['embedding'])
            return all_embeddings
        except Exception as e:
            logger.error(f"Gemini embedding API error: {e}")
            raise e

    def generate_response(self, prompt: str) -> Dict[str, Any]:
        try:
            response = self.model.generate_content(prompt)
            logger.info("Gemini API call successful")
            return {
                "answer": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                }
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise e
