from .gemini_provider import AIProvider, GeminiProvider
from ...core.config import get_settings


def get_ai_provider() -> AIProvider:
    settings = get_settings()
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)
