
import chromadb
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# 1. Load the embedding model
# --------------------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------------------------
# 2. Connect to a persistent database
# --------------------------------------------------
client = chromadb.PersistentClient(path="./data/chroma_demo")

# --------------------------------------------------
# 3. Create or open a collection
# --------------------------------------------------
collection = client.get_or_create_collection(
    name="learning_documents",
    metadata={"hnsw:space": "cosine"}
)

# --------------------------------------------------
# 4. Insert sample documents with metadata
# --------------------------------------------------
documents = [
    "Python is a popular programming language.",
    "FastAPI is used to build APIs with Python.",
    "RAG retrieves relevant documents for language models.",
    "Embeddings convert text into numerical vectors.",
    "ChromaDB stores and searches vector embeddings.",
    "Cosine similarity compares vector directions.",
    "Chunking splits documents into smaller pieces.",
    "Metadata provides additional information about documents.",
    "Citations identify the sources used in an answer.",
    "GraphRAG uses relationships between entities and information."
]

ids = [f"doc{i}" for i in range(1, 11)]

metadatas = [
    {"topic": "python", "source": "python.md"},
    {"topic": "api", "source": "api.md"},
    {"topic": "rag", "source": "rag.md"},
    {"topic": "embeddings", "source": "embeddings.md"},
    {"topic": "vector_database", "source": "chroma.md"},
    {"topic": "embeddings", "source": "similarity.md"},
    {"topic": "rag", "source": "chunking.md"},
    {"topic": "metadata", "source": "metadata.md"},
    {"topic": "citations", "source": "citations.md"},
    {"topic": "graphrag", "source": "graphrag.md"},
]

embeddings = model.encode(
    documents,
    normalize_embeddings=True
).tolist()

collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print("\n1. INSERT DOCUMENTS")
print("Total records:", collection.count())

# --------------------------------------------------
# 5. Search using similarity
# --------------------------------------------------
query = "How does retrieval work?"

query_embedding = model.encode(
    [query],
    normalize_embeddings=True
).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

print("\n2. SIMILARITY SEARCH")

for doc_id, document, metadata, distance in zip(
    results["ids"][0],
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print(f"\nID: {doc_id}")
    print(f"Document: {document}")
    print(f"Metadata: {metadata}")
    print(f"Distance: {distance:.4f}")

# --------------------------------------------------
# 6. Filter documents by metadata
# --------------------------------------------------
print("\n3. METADATA FILTERING")

for topic in ["rag", "embeddings", "citations"]:
    filtered_results = collection.query(
        query_embeddings=query_embedding,
        n_results=5,
        where={"topic": topic},
        include=["documents", "metadatas", "distances"]
    )

    print(f"\nTopic: {topic}")

    for document, metadata in zip(
        filtered_results["documents"][0],
        filtered_results["metadatas"][0]
    ):
        print(f"- {document}")
        print(f"  Metadata: {metadata}")

# --------------------------------------------------
# 7. Update a document using upsert()
# --------------------------------------------------
print("\n4. UPDATE DOCUMENT")

updated_document = (
    "RAG retrieves relevant information and supplies "
    "it to a language model as context."
)

updated_embedding = model.encode(
    [updated_document],
    normalize_embeddings=True
).tolist()

collection.upsert(
    ids=["doc3"],
    documents=[updated_document],
    embeddings=updated_embedding,
    metadatas=[
        {
            "topic": "rag",
            "source": "rag-intro-updated.md"
        }
    ]
)

updated_record = collection.get(
    ids=["doc3"],
    include=["documents", "metadatas"]
)

print("Updated document:", updated_record["documents"][0])
print("Updated metadata:", updated_record["metadatas"][0])

# --------------------------------------------------
# 8. Delete a test record safely
# --------------------------------------------------
print("\n5. DELETE A TEST RECORD")

test_document = "Temporary record for deletion testing."

test_embedding = model.encode(
    [test_document],
    normalize_embeddings=True
).tolist()

collection.upsert(
    ids=["test-delete"],
    documents=[test_document],
    embeddings=test_embedding,
    metadatas=[
        {
            "topic": "test",
            "source": "temporary.md"
        }
    ]
)

collection.delete(ids=["test-delete"])

deleted_record = collection.get(ids=["test-delete"])

print("Deleted record IDs:", deleted_record["ids"])
print("Record successfully deleted:", not deleted_record["ids"])

# --------------------------------------------------
# 9. Check persistence
# --------------------------------------------------
print("\n6. PERSISTENCE CHECK")

print("Collection:", collection.name)
print("Database path: ./data/chroma_demo")
print("Remaining records:", collection.count())

saved_records = collection.get(
    limit=10,
    include=["documents", "metadatas"]
)

for record_id, document, metadata in zip(
    saved_records["ids"],
    saved_records["documents"],
    saved_records["metadatas"]
):
    print(f"\nID: {record_id}")
    print(f"Document: {document}")
    print(f"Metadata: {metadata}")

print("\nAll exercises completed!")
