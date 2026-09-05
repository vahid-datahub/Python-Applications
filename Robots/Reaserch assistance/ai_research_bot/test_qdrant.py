from app.services.vector_store.qdrant_store import QdrantStore
from app.services.embedding.ollama_provider import OllamaEmbeddingProvider

texts = [
    "Artificial intelligence is used in research.",
    "Machine learning is a branch of artificial intelligence.",
    "Traffic congestion affects urban transportation."
]

provider = OllamaEmbeddingProvider()

embeddings = provider.embed(texts)

store = QdrantStore()

store.create_collection(
    vector_size=len(embeddings[0])
)

document_id = "test-document"

store.add_documents(
    document_id=document_id,
    chunks=texts,
    embeddings=embeddings
)

query = "What is machine learning?"

query_embedding = provider.embed([query])[0]

results = store.search(
    query_embedding=query_embedding,
    limit=2,
    document_id=document_id
)

for result in results:
    print("\n--- Result ---")
    print("Score:", result.score)
    print("Text:", result.payload["text"])