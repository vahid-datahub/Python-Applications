import ollama
from app.services.llm.base import LLMProvider

class OllamaLLMProvider(LLMProvider):

    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = ollama.generate(model=self.model_name, prompt=prompt)

        return response["response"]