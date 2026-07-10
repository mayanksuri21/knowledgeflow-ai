from abc import ABC, abstractmethod
from typing import List, Dict


class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> str:
        pass


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_response(self, prompt: str, context: str) -> str:
        # In Version 1, return a placeholder
        # Later, integrate with actual Gemini API
        return "AI response placeholder"
