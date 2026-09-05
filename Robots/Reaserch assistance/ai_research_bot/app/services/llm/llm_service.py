from app.services.llm.base import LLMProvider

class LLMService:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate_answer(self, prompt: str) -> str:
        if not prompt.strip():
            return ""

        return self.provider.generate(prompt)
    
