from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "How can I reset my password?",
    "Steps to change a forgotten password.",
    "What is the weather today?",
]

# Generate one embedding for each sentence.
embeddings = model.encode(sentences)

print("Number of sentences:", len(sentences))
print("Embedding matrix shape:", embeddings.shape)

# Compare the first sentence with every sentence.
scores = cosine_similarity(
    embeddings[0].reshape(1, -1),
    embeddings
)[0]

print("\nSimilarity scores:")

for sentence, score in zip(sentences, scores):
    print(f"{score:.4f} - {sentence}")