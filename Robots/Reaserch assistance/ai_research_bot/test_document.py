from pathlib import Path
from app.services.document_processor import DocumentProcessor


processor = DocumentProcessor()

file_path = Path("documents/Exploring Lightweight Federated Learning for.pdf")

text = processor.extract_text(file_path)

print(text[:3000])