
# Lesson 5: Vector Similarity

## 5.1 What is Vector Similarity?

Vector similarity measures how similar two vectors are based on their direction, distance, or mathematical relationship.

In Retrieval-Augmented Generation (RAG), vector similarity helps find document chunks that are semantically related to a user's question.

An embedding model converts text into numerical vectors. A similarity measure compares these vectors to identify relevant information.

### Example

User question:
"How can I reset my password?"

Document 1:
"Users can recover their account by resetting their password."

Document 2:
"How to prepare a vegetable salad."

The embedding of Document 1 will generally be more semantically similar to the question than the embedding of Document 2.

The retrieval system uses similarity scores or distances to rank the document chunks.

## 5.2 What is a Vector?

A vector is an ordered list of numerical values representing information.

Example:

```python
vector_a = [0.2, 0.5, 0.8]
vector_b = [0.3, 0.6, 0.7]
```

In machine learning, an embedding model generates vectors from text, images, or other data.

For text embeddings, each dimension represents a learned feature of the text. Individual dimensions usually do not have simple, directly interpretable meanings.

## 5.3 Common Vector Similarity Methods

The three commonly used methods are:

1. Cosine similarity
2. Dot product
3. Euclidean distance

### A. Cosine Similarity

Cosine similarity measures the angle between two nonzero vectors.

Formula:

cosine(A, B) = (A · B) / (||A|| × ||B||)

Where:

- A and B are vectors.
- A · B is the dot product of the vectors.
- ||A|| is the magnitude (length) of vector A.
- ||B|| is the magnitude (length) of vector B.

For nonzero vectors, cosine similarity ranges from -1 to 1.

Interpretation:

- Close to 1: vectors point in similar directions.
- Close to 0: vectors are perpendicular.
- Close to -1: vectors point in opposite directions.

For many text embedding models, higher cosine similarity often indicates greater semantic similarity.

However, the interpretation depends on the embedding model and dataset.

### B. Dot Product

The dot product multiplies corresponding vector values and adds the results.

Formula:

A · B = A1B1 + A2B2 + ... + AnBn

Example:

```python
import numpy as np

vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])

score = np.dot(vector_a, vector_b)

print(score)
# Output: 32
```

Dot product considers both vector direction and magnitude.

When vectors are normalized to have a length of 1, their dot product equals their cosine similarity.

Dot product is commonly used in embedding retrieval systems.

### C. Euclidean Distance

Euclidean distance measures the straight-line distance between two vectors.

Formula:

d(A, B) = sqrt(sum((Ai - Bi)^2))

Example:

```python
import numpy as np

vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])

distance = np.linalg.norm(vector_a - vector_b)

print(round(distance, 4))
# Output: 5.1962
```

Interpretation:

- Smaller distance: vectors are closer.
- Larger distance: vectors are farther apart.

In many embedding retrieval systems, smaller Euclidean distances indicate more similar vectors, but this depends on the embedding representation and retrieval setup.

## 5.4 Cosine Similarity Using Python

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

vector_a = np.array([[1, 2, 3]])
vector_b = np.array([[4, 5, 6]])

score = cosine_similarity(vector_a, vector_b)[0][0]

print("Cosine Similarity:", round(score, 4))
```

Expected output:

```text
Cosine Similarity: 0.9746
```

The score indicates that the vectors point in similar directions.

Note: These are simple numerical vectors used for demonstration, not actual text embeddings.

## 5.5 Comparing the Three Methods

| Method | Measures | Better match |
|---|---|---|
| Cosine similarity | Angle between vectors | Usually higher score |
| Dot product | Direction and magnitude | Usually higher score |
| Euclidean distance | Straight-line distance | Usually lower distance |

Important:

Cosine similarity and dot product produce higher-is-better scores. Euclidean distance is a distance measure, so lower is generally better.

Do not compare raw scores from different methods as if they were equivalent.

## 5.6 Vector Similarity in RAG

A typical RAG retrieval process works as follows:

1. Collect documents from approved sources.
2. Split documents into smaller chunks.
3. Generate an embedding for each chunk.
4. Store the embeddings and associated text in a vector database.
5. Convert the user's question into an embedding using a compatible embedding model.
6. Compare the question embedding with stored document embeddings.
7. Rank the matching chunks.
8. Retrieve the most relevant chunks.
9. Pass the retrieved context to the LLM.
10. Generate an answer grounded in the retrieved information.

### RAG Architecture

```text
Documents
    |
    v
Document Chunking
    |
    v
Embedding Model
    |
    v
Vector Database
    ^
    |
Question Embedding
    ^
    |
User Question
    |
    v
Similarity Search
    |
    v
Top-K Relevant Chunks
    |
    v
LLM + Retrieved Context
    |
    v
Final Answer with Citations
```





## 5.8 Important Concepts to Remember

- An embedding represents information as a numerical vector.
- Vector similarity helps identify related information.
- Cosine similarity compares vector directions.
- Dot product considers both direction and magnitude.
- Euclidean distance measures the distance between vectors.
- Similarity scores depend on the embedding model and retrieval method.
- The query and document embeddings must be compatible.
- A high similarity score does not guarantee that a document fully answers the question.
- Top-K retrieval selects a specified number of highly ranked results.
- RAG uses retrieved chunks as context for generating answers.
- Citations should point to the actual source documents used to support the answer.

## 5.9 Lesson Summary

Vector similarity is a key concept in semantic search and RAG. It helps a retrieval system find document chunks related to a user's question by comparing their embeddings.

Cosine similarity, dot product, and Euclidean distance are common comparison methods. Understanding their differences helps us build better retrieval systems.


