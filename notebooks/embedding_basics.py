from sentence_transformers import SentenceTransformer

# Load a sentence embedding model.
# The model may be downloaded the first time it runs.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

text = "How can I reset my password?"

# Generate an embedding vector.
embedding = model.encode(text)

print("Input text:", text)
print("Embedding type:", type(embedding))
print("Embedding dimensions:", embedding.shape)
print("First 10 values:", embedding[:10])