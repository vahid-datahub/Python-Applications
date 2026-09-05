from app.services.embedding.ollama_provider import OllamaEmbeddingProvider
from app.services.embedding.embedding_service import EmbeddingService

from app.services.vector_store.qdrant_store import QdrantStore

from app.services.retrieval.retrieval_service import RetrievalService

from app.services.llm.ollama_provider import OllamaLLMProvider
from app.services.llm.llm_service import LLMService

from app.services.rag.rag_service import RAGService


# Embedding
embedding_provider = OllamaEmbeddingProvider()
embedding_service = EmbeddingService(embedding_provider)

# Vector Store
vector_store = QdrantStore()

# Retrieval
retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store
)

# LLM
llm_provider = OllamaLLMProvider()
llm_service = LLMService(
    provider=llm_provider
)

# RAG
rag_service = RAGService(
    retrieval_service=retrieval_service,
    llm_service=llm_service
)


question = "What is the main topic of this paper?"

answer = rag_service.answer_question(
    question=question,
    document_id="test-document",
    limit=5
)

print("\n--- Answer ---")
print(answer)