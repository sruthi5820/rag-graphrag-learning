import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="vector_database_exercises"
)

questions = [
    "What is an embedding?",
    "How is text converted into numbers?",
    "Explain numerical representations of text.",
    "How does a vector database work?",
]

collection_count = collection.count()

if collection_count == 0:
    print("The collection is empty. Add documents first.")
    raise SystemExit(1)

top_k = min(3, collection_count)

for question in questions:
    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 70)
    print(f"Question: {question}")
    print("=" * 70)

    for rank, (doc_id, document, metadata, distance) in enumerate(
        zip(ids, documents, metadatas, distances),
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(f"Document ID: {doc_id}")
        print(f"Distance: {distance:.4f}")
        print(f"Metadata: {metadata}")
        print(f"Content: {document[:200]}")