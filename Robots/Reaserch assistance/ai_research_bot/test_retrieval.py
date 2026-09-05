from app.services.embedding.ollama_provider import OllamaEmbeddingProvider
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_store import QdrantStore
from app.services.retrieval.retrieval_service import RetrievalService


provider = OllamaEmbeddingProvider()

embedding_service = EmbeddingService(provider)

vector_store = QdrantStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store
)

query = "What is machine learning?"

results = retrieval_service.retrieve(
    query=query,
    limit=2,
    document_id="test-document"
)

for result in results:
    print("\n--- Result ---")
    print("Score:", result.score)
    print("Text:", result.payload["text"])