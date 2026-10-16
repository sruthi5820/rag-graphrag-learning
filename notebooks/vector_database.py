import chromadb

# Create or open a persistent local Chroma database.
client = chromadb.PersistentClient(
    path="./data/chroma_demo"
)

# Create the collection if it does not already exist.
collection = client.get_or_create_collection(
    name="learning_documents"
)

# Insert or update records using stable IDs.
collection.upsert(
    ids=["doc1", "doc2"],
    documents=[
        "RAG retrieves relevant documents before answering.",
        "Graph databases represent entities and relationships.",
    ],
    metadatas=[
        {"topic": "rag", "source": "rag-intro.md"},
        {"topic": "graphrag", "source": "graph-intro.md"},
    ],
)

# Search the collection.
results = collection.query(
    query_texts=[
        "How does document retrieval help an LLM?"
    ],
    n_results=2,
)

print("Search results:\n")

for document, metadata in zip(
    results["documents"][0],
    results["metadatas"][0],
):
    print("Document:", document)
    print("Metadata:", metadata)
    print("-" * 50)



""""
### What Happens?

1. Chroma opens or creates the persistent database.
2. The script creates the `learning_documents` collection if necessary.
3. Two documents and their metadata are inserted or updated.
4. Chroma generates embeddings using its configured default embedding function, if available.
5. The query is embedded using the compatible query embedding function.
6. Chroma searches the collection and returns up to two results.

For this introductory exercise, the default embedding function is used. Its availability and model-download behavior depend on the installed Chroma version and environment.

Later, configure an explicit embedding model and use a compatible configuration for both indexing and querying.

### Expected Output

The exact ranking may vary, but the output should contain the stored documents and their metadata.

```text
Search results:

Document: RAG retrieves relevant documents before answering.
Metadata: {'topic': 'rag', 'source': 'rag-intro.md'}
--------------------------------------------------
...
```

### Key Learning

You created a persistent vector collection, stored text and metadata, and retrieved documents using a semantic query.

"""