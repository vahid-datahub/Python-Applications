import ollama
from app.services.embedding.base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.model_name = model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = ollama.embed(model=self.model_name, input=texts)
        return response["embeddings"]
    