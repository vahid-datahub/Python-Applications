from app.services.text_chunker import TextChunker


chunker = TextChunker(
    chunk_size=1000,
    chunk_overlap=200
)

text = """
This is a sample research paper text.
We are testing the text chunking process.
The document will eventually be divided into smaller chunks
for embedding and retrieval.
""" * 100

chunks = chunker.split_text(text)

print(f"Number of chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk[:100])