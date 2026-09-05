from app.services.embedding.ollama_provider import OllamaEmbeddingProvider
from app.services.embedding.embedding_service import EmbeddingService


provider = OllamaEmbeddingProvider()

embedding_service = EmbeddingService(provider)

texts = [
    "This is a research paper about artificial intelligence.",
    "This paper discusses machine learning algorithms."
]

embeddings = embedding_service.create_embeddings(texts)

print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimension: {len(embeddings[0])}")