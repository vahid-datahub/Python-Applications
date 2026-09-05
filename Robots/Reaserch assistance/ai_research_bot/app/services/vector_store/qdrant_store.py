from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

class QdrantStore:

    def __init__(self,storage_path: str = "qdrant_data", collection_name: str = "research_documents"):
        self.client = QdrantClient(path=storage_path)
        self.collection_name = collection_name

    def create_collection(self, vector_size: int):
        collections = self.client.get_collections().collections
        collection_exists = any(collection.name == self.collection_name
            for collection in collections)

        if not collection_exists:
            self.client.create_collection(collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size,distance=Distance.COSINE))

    def add_documents(self, document_id: str, chunks: list[str], embeddings: list[list[float]]):
        if not chunks or not embeddings:
            return

        points = []
        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = str(uuid.uuid4())
            points.append(PointStruct(id=chunk_id, vector=embedding,
                    payload={
                        "document_id": document_id,
                        "chunk_index": index,
                        "text": chunk
                    }))

        self.client.upsert(collection_name=self.collection_name,points=points)
    
    
    def search(self,query_embedding: list[float],limit: int = 5,document_id: str | None = None):
        query_filter = None

        if document_id:
            query_filter = Filter(must=[FieldCondition(key="document_id",match=MatchValue(value=document_id))])

        results = self.client.query_points(collection_name=self.collection_name,query=query_embedding,
            query_filter=query_filter,limit=limit)
        return results.points