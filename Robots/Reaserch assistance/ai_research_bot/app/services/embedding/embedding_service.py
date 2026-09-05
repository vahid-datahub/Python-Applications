from app.services.embedding.base import EmbeddingProvider


class EmbeddingService:

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        return self.provider.embed(texts)