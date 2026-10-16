from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

query = "How do I recover my account?"

documents = [
    "Users can reset a forgotten password through account recovery.",
    "The weather forecast predicts rain tomorrow.",
    "Contact the support team for help with technical problems.",
    "The training department publishes learning materials.",
]

# Generate the query embedding.
query_embedding = model.encode([query])

# Generate embeddings for all documents.
document_embeddings = model.encode(documents)

# Calculate similarity scores.
scores = cosine_similarity(
    query_embedding,
    document_embeddings
)[0]

# Sort documents from most similar to least similar.
ranked_results = sorted(
    zip(documents, scores),
    key=lambda item: item[1],
    reverse=True,
)

print("Query:", query)
print("\nRanked results:")

for rank, (document, score) in enumerate(ranked_results, start=1):
    print(f"{rank}. Score: {score:.4f}")
    print(f"   Document: {document}")
