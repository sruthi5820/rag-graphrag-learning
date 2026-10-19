sources = [
    {
        "source_id": "S1",
        "document_id": "doc_001",
        "chunk_id": "chunk_001",
        "title": "RAG Introduction",
        "text": "RAG retrieves relevant documents for an LLM.",
        "url": "https://example.org/rag",
        "page": 3,
    },
    {
        "source_id": "S2",
        "document_id": "doc_002",
        "chunk_id": "chunk_002",
        "title": "Embedding Guide",
        "text": "Embeddings represent text as numerical vectors.",
        "url": "https://example.org/embeddings",
        "page": 5,
    },
]

for source in sources:
    print("\nSource ID:", source["source_id"])
    print("Document ID:", source["document_id"])
    print("Chunk ID:", source["chunk_id"])
    print("Title:", source["title"])
    print("Text:", source["text"])
    print("URL:", source["url"])
    print("Page:", source["page"])