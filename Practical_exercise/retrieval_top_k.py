
#Understand how requesting 3, 5, or 10 results changes the number of chunks retrieved and the amount of useful evidence found.
import chromadb

# Connect to the existing persistent database.
client = chromadb.PersistentClient(path="./chroma_db")

# Open the existing collection.
collection = client.get_collection(
    name="vector_database_exercises"
)

question = "How does retrieval work?"

collection_count = collection.count()

if collection_count == 0:
    print("The collection is empty. Add documents first.")
    raise SystemExit(1)

print(f"Collection document count: {collection_count}")
print(f"Question: {question}")

# Compare different top-k values.
for requested_top_k in [3, 5, 10]:
    # Do not request more results than the collection contains.
    top_k = min(requested_top_k, collection_count)

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
    print(f"Requested top-k: {requested_top_k}")
    print(f"Actual results returned: {len(ids)}")
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