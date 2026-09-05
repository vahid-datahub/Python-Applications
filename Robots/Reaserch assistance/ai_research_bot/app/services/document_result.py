from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentResult:
    document_id: str
    file_name: str
    file_path: Path
    text: str
    character_count: int
    chunks: list[str]
    embeddings: list[list[float]]