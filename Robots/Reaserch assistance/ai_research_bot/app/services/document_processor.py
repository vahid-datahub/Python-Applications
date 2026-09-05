from pathlib import Path
import pymupdf
from docx import Document
from app.services.document_result import DocumentResult
from app.services.text_chunker import TextChunker
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_store import QdrantStore
import uuid


class DocumentProcessor:
    def __init__(self,embedding_service: EmbeddingService, vector_store: QdrantStore):
        self.text_chunker = TextChunker(chunk_size=1000,chunk_overlap=200)
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def extract_document(self, file_path: Path) -> DocumentResult:
        file_extension = file_path.suffix.lower()

        if file_extension == ".pdf":
            text = self._extract_pdf_text(file_path)

        elif file_extension == ".docx":
            text = self._extract_docx_text(file_path)

        else:
            raise ValueError("Unsupported document format.")

        chunks = self.text_chunker.split_text(text)
        embeddings = self.embedding_service.create_embeddings(chunks)
        self.vector_store.create_collection(vector_size=len(embeddings[0]))
        document_id = str(uuid.uuid4())
        self.vector_store.add_documents(document_id=document_id, chunks=chunks, embeddings=embeddings)
        
        return DocumentResult(document_id=document_id, file_name=file_path.name, file_path=file_path, 
            text=text, character_count=len(text), chunks=chunks, embeddings=embeddings)

    def _extract_pdf_text(self, file_path: Path) -> str:
        text = []
        pdf_document = pymupdf.open(file_path)

        for page in pdf_document:
            text.append(page.get_text())
        pdf_document.close()

        return "\n".join(text)

    def _extract_docx_text(self, file_path: Path) -> str:
        document = Document(file_path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]

        return "\n".join(paragraphs)