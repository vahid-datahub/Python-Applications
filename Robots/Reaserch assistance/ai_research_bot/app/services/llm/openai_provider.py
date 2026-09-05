import os
from openai import OpenAI
from app.services.llm.base import LLMProvider

class OpenAILLMProvider(LLMProvider):

    def __init__(self, model_name: str = "gpt-5.6-luna"):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model_name,input=prompt)

        return response.output_text