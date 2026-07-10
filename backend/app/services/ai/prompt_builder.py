class PromptBuilder:
    def build_prompt(self, query: str, context: str) -> str:
        return f"""
        Context: {context}
        
        User Query: {query}
        
        Please answer based on the provided context.
        """
