import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="vector_database_exercises"
)

question = "How does retrieval work?"

collection_count = collection.count()

if collection_count == 0:
    print("The collection is empty. Add documents first.")
    raise SystemExit(1)


def print_results(title, results):
    """Print the IDs, topics, distances, and text of search results."""

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 70)
    print(title)
    print(f"Number of results: {len(ids)}")
    print("=" * 70)

    if not ids:
        print("No matching documents found.")
        return

    for rank, (doc_id, document, metadata, distance) in enumerate(
        zip(ids, documents, metadatas, distances),
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(f"Document ID: {doc_id}")
        print(f"Topic: {metadata.get('topic')}")
        print(f"Distance: {distance:.4f}")
        print(f"Content: {document[:200]}")


# Search without a metadata filter.
unfiltered = collection.query(
    query_texts=[question],
    n_results=min(5, collection_count),
    include=["documents", "metadatas", "distances"],
)

# Search only documents tagged with topic="rag".
filtered = collection.query(
    query_texts=[question],
    n_results=min(5, collection_count),
    where={"topic": "rag"},
    include=["documents", "metadatas", "distances"],
)

print(f"Question: {question}")

print_results("UNFILTERED SEARCH", unfiltered)
print_results("FILTERED SEARCH: topic = rag", filtered)

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)

unfiltered_ids = unfiltered["ids"][0]
filtered_ids = filtered["ids"][0]

print("Unfiltered IDs:", unfiltered_ids)
print("Filtered IDs:", filtered_ids)

removed_ids = [
    doc_id for doc_id in unfiltered_ids
    if doc_id not in filtered_ids
]

print("Unfiltered results absent from filtered results:", removed_ids)