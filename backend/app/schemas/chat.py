from pydantic import BaseModel
from typing import Dict, Any


class ChatQuestion(BaseModel):
    question: str


class ChatUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int


class ChatAnswer(BaseModel):
    answer: str
    document_id: str
    usage: ChatUsage
