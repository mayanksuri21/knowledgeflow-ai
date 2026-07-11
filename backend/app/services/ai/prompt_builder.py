from typing import Optional


class PromptBuilder:
    @staticmethod
    def build_prompt(question: str, document_context: str) -> str:
        return f"""You are a helpful assistant that answers questions based only on the provided document.

Instructions:
1. Read the document carefully.
2. Answer the user's question using only information from the document.
3. If the answer cannot be found in the document, clearly state: "I couldn't find the answer in the provided document."
4. Do not use any external knowledge.
5. Be concise and accurate.

Document content:
{document_context}

User's question: {question}

Please provide your answer:"""
