from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_store import QdrantStore


class RetrievalService:

    def __init__(self,embedding_service: EmbeddingService, vector_store: QdrantStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self,query: str,limit: int = 5,document_id: str | None = None):
        query_embedding = self.embedding_service.create_embeddings([query])[0]

        return self.vector_store.search(query_embedding=query_embedding,
            limit=limit,document_id=document_id)