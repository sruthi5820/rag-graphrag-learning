
# Lesson 4: Embeddings

## 4.1 What Are Embeddings?

Embeddings are numerical vectors that represent data such as text, images, audio, or other information.

In Natural Language Processing (NLP), **text embeddings represent aspects of the meaning of text as numerical vectors**.

These vectors allow computers to compare text and identify content with related meanings.

In a Retrieval-Augmented Generation (RAG) system, embeddings help find document passages that are semantically related to a user's question.

### Example

Consider these sentences:

1. "How can I reset my password?"
2. "Steps to change a forgotten password."
3. "What is the weather today?"

The first two sentences have related meanings. A suitable embedding model will often represent them more similarly than the weather sentence.

### Simple Explanation

A computer does not naturally understand sentences in the same way a human does. An embedding model converts text into numbers that machine-learning systems can compare.

Example:

```text
Input:
"How can I reset my password?"

Embedding model:
        |
        v

[0.12, -0.08, 0.41, 0.27, ...]
```

The numbers shown are illustrative only. Real embeddings usually contain many dimensions, and their values depend on the model.

### Key Learning

Embeddings convert data into numerical representations that make similarity comparison possible.

---

## 4.2 Why Do We Need Embeddings?

Traditional keyword search mainly looks for matching words or terms.

Semantic search attempts to find information based on meaning, even when the query and document use different words.

### Example

User question:

```text
How can I reset my password?
```

Available documents:

```text
Document 1:
Steps to change a forgotten password.

Document 2:
Today's weather forecast.

Document 3:
How to update your account password.
```

A semantic retrieval system may identify Documents 1 and 3 as relevant even though they do not contain exactly the same wording as the question.

### Without Embeddings

A basic keyword search might look for matching terms such as:

- Reset
- Password

It can work well when important words match, but it may miss relevant passages that use different wording.

### With Embeddings

The system converts the question and documents into vectors and compares their semantic similarity.

This can help identify relevant information even when the wording differs.

### Benefits of Embeddings

- Support semantic search.
- Help retrieve relevant document chunks.
- Find similar questions or documents.
- Support recommendation systems.
- Help group related content.
- Improve retrieval when query and document wording differ.

### Important Note

Embeddings do not guarantee that two semantically related sentences will always have similar vectors. Quality depends on the embedding model, the language, the domain, and how the text is prepared.

---

## 4.3 How Does an Embedding Model Work?

An embedding model is a machine-learning model that converts supported input data into a numerical vector.

### Basic Workflow

```text
Input Text
    |
    v
Embedding Model
    |
    v
Numerical Vector
    |
    v
Store or Compare Vector
    |
    v
Find Similar Content
```

### Step 1: Prepare the Text

Example:

```text
How can I reset my password?
```

The text is supplied to the embedding model.

### Step 2: Process the Text

The model tokenizes and processes the input according to its architecture.

### Step 3: Generate an Embedding

The model returns a vector containing numerical values.

Illustrative example:

```text
[0.12, -0.08, 0.41, 0.27, -0.16]
```

This is a simplified vector with five dimensions. A real model may produce hundreds or thousands of dimensions.

### Step 4: Store the Embedding

For document retrieval, the application stores the vector alongside the corresponding text and metadata.

### Step 5: Embed the User's Question

When a user asks a question, the same embedding model is normally used to generate a query vector.

### Step 6: Compare Vectors

The retrieval system compares the query vector with stored document vectors using a similarity or distance measure.

### Step 7: Retrieve Relevant Text

The system returns the text associated with the most relevant vectors.

### Key Learning

An embedding model transforms text into vectors. A retrieval system compares those vectors and uses the results to find relevant content.

---

## 4.4 What Is a Vector?

A vector is an ordered collection of numerical values.

Example:

```text
[0.12, -0.08, 0.41, 0.27]
```

This vector has four dimensions.

Each embedding dimension is part of a learned numerical representation. Individual dimensions generally should not be interpreted as simple human-readable concepts.

### Important Vector Properties

- **Dimension:** The number of values in a vector.
- **Magnitude:** The length of the vector.
- **Direction:** The orientation of the vector in its mathematical space.
- **Similarity:** A measure of how related two vectors are under a chosen metric.

### Example

Suppose we have two illustrative vectors:

```text
A = [1, 2]
B = [2, 4]
```

Vector B is twice vector A, so they point in the same direction.

Their cosine similarity is 1, even though their magnitudes differ.

Now consider:

```text
C = [-1, -2]
```

Vector C points in the opposite direction from A, giving a cosine similarity of -1.

These are simple mathematical examples, not real text embeddings.

### Key Learning

Vectors are numerical representations. Their relationships can be analyzed using mathematical operations.

---

## 4.5 What Is Embedding Dimension?

Embedding dimension is the number of numerical values in an embedding vector.

For example:

```text
[0.12, -0.08, 0.41]
```

This vector has three dimensions.

Another vector:

```text
[0.12, -0.08, 0.41, 0.27, -0.16]
```

has five dimensions.

### Why Does Dimension Matter?

Dimension affects:

- Storage requirements.
- Memory usage.
- Similarity-search computation.
- Index size.
- Retrieval performance and quality.

A larger dimension does not automatically mean a better embedding.

### Example

If a model generates 768-dimensional embeddings, every vector generated by that model normally contains 768 values.

If each value is stored as a 32-bit floating-point number, the raw vector data requires approximately:

```text
768 dimensions × 4 bytes = 3,072 bytes
```

That is approximately 3 KB per vector, excluding metadata, indexing, and storage overhead.

For 100,000 such vectors:

```text
3,072 bytes × 100,000
= 307,200,000 bytes
```

This is approximately 307 MB in decimal units for the raw vector values alone.

### Important Point

The embedding dimension is determined by the model or its configured output. Do not arbitrarily change the vector length when storing or comparing embeddings.

---

## 4.6 Word Embeddings vs Sentence Embeddings

Embedding techniques can represent words, sentences, passages, and other forms of data.

### Word Embeddings

Word embeddings represent individual words or tokens as vectors.

Classic approaches include Word2Vec and GloVe.

They are useful for learning relationships between words, although a single vector per word may not adequately represent different meanings in different contexts.

Example:

The word "bank" can refer to a financial institution or the side of a river.

A static word embedding generally gives the word the same learned vector regardless of the sentence.

### Contextual Representations

Transformer-based models can produce representations that depend on surrounding words.

For example:

```text
I deposited money at the bank.
```

```text
We sat on the river bank.
```

The word "bank" is used differently in these sentences. Contextual models can represent these different uses differently.

### Sentence Embeddings

Sentence embedding models produce a single vector representing a sentence or text passage.

Example:

```text
"How can I reset my password?"
```

The model generates one vector for the input sentence.

Sentence embeddings are widely used in semantic search and RAG systems.

### Comparison

| Feature | Word Embedding | Sentence Embedding |
|---|---|---|
| Typical input | Individual word or token | Sentence or passage |
| Typical output | Vector per word or token | Vector for the complete input |
| Main use | Word relationships and language processing | Semantic search and text similarity |
| RAG usage | Less common as a direct retrieval representation | Common for query and document retrieval |

### Key Learning

Sentence embeddings are commonly used in RAG because the application needs to compare complete questions with document chunks.

---

## 4.7 What Is Semantic Similarity?

Semantic similarity measures how closely related two pieces of text are in meaning.

An embedding model represents both texts as vectors. A similarity function compares those vectors.

### Example

Text A:

```text
How can I reset my password?
```

Text B:

```text
How do I change my forgotten password?
```

These sentences express similar intentions.

Text C:

```text
What is the weather today?
```

This sentence has a different meaning.

A suitable embedding model will often produce a stronger similarity score for A and B than for A and C.

### Important Distinction

Semantic similarity is not exactly the same as:

- Exact word matching.
- Factual correctness.
- Logical equivalence.
- Relevance to every possible question.

Two sentences can discuss similar topics while expressing different or contradictory facts.

For example:

```text
The service is available.
```

```text
The service is not available.
```

These sentences are topically similar, but their meanings differ in a critical way.

### Key Learning

Embedding similarity helps estimate semantic relatedness. It does not independently verify whether information is true.

---

## 4.8 Cosine Similarity

Cosine similarity is a common method for comparing two vectors.

It measures the cosine of the angle between them.

The formula is:

cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

Where:

- A and B are vectors.
- A · B is their dot product.
- ||A|| and ||B|| are their magnitudes.

### How to Interpret Cosine Similarity

For nonzero vectors, cosine similarity ranges from -1 to 1.

| Score | General interpretation |
|---|---|
| Close to 1 | Vectors point in similar directions |
| Close to 0 | Vectors are approximately perpendicular |
| Close to -1 | Vectors point in opposite directions |

For many modern text embedding models, useful text similarities often fall within a narrower range. The exact scores depend on the model and dataset.

### Example

Consider:

```text
A = [1, 0]
B = [1, 0]
```

The vectors point in the same direction.

Cosine similarity = 1.

Now consider:

```text
A = [1, 0]
C = [0, 1]
```

The vectors are perpendicular.

Cosine similarity = 0.

Finally:

```text
A = [1, 0]
D = [-1, 0]
```

The vectors point in opposite directions.

Cosine similarity = -1.

### Why Is Cosine Similarity Used in RAG?

It can help rank document embeddings according to their similarity to a query embedding.

The system can then retrieve the highest-ranked document chunks.

### Important Note

A cosine similarity score is not automatically a probability or a percentage of correctness. Do not interpret a score of 0.8 as an 80% chance that a document is correct.

---

## 4.9 Other Similarity and Distance Measures

Cosine similarity is not the only way to compare vectors.

### 1. Dot Product

The dot product multiplies corresponding vector values and sums the results.

It is often used in vector search systems.

Unlike cosine similarity, the dot product can be affected by vector magnitudes.

### 2. Euclidean Distance

Euclidean distance measures the straight-line distance between two vectors.

For vectors A and B:

distance(A, B) = sqrt(sum((A[i] - B[i])²))

A smaller distance means the vectors are closer under this metric.

### Comparison

| Metric | What it measures | Typical ranking preference |
|---|---|---|
| Cosine similarity | Directional similarity | Higher is better |
| Dot product | Vector product | Higher is often better |
| Euclidean distance | Straight-line distance | Lower is better |

### Which Metric Should You Use?

Follow the embedding model's recommendations and the vector database's supported configuration.

Some systems normalize vectors, making cosine similarity and dot-product ranking equivalent under suitable conditions.

Do not mix incompatible metrics or assume that scores from different models are directly comparable.

---

## 4.10 What Is an Embedding Model?

An embedding model is a trained model that generates vector representations for input data.

Different models can vary in:

- Embedding dimensions.
- Supported languages.
- Maximum input length.
- Retrieval quality.
- Domain performance.
- Speed.
- Memory requirements.
- Hardware requirements.
- License and deployment options.

### Examples of Text Embedding Models

- Sentence Transformers models.
- `all-MiniLM-L6-v2`.
- BGE model families.
- E5 model families.
- Nomic embedding models.

These are examples, not a ranking. The best choice depends on the use case and evaluation results.

### What Should You Consider When Choosing a Model?

1. Does it perform well for your language and domain?
2. Can it handle your expected document chunk size?
3. Does it support query and document embedding in the required way?
4. Is its vector dimension compatible with your index?
5. Can it run within your hardware limits?
6. Does its license permit your intended use?
7. Does it provide good retrieval results on your test questions?

### Important Point

Changing the embedding model usually requires regenerating document embeddings and rebuilding or migrating the vector index.

Vectors from different models should not be mixed in one index unless the system is specifically designed to handle them.

---

## 4.11 What Is Semantic Search?

Semantic search retrieves content based on meaning rather than relying only on exact keyword matches.

### Semantic Search Workflow

```text
User Query
    |
    v
Create Query Embedding
    |
    v
Search Document Vectors
    |
    v
Rank Similarity Results
    |
    v
Return Relevant Text
```

### Example

User query:

```text
How do I change a forgotten password?
```

Available documents:

```text
Document A:
Password recovery instructions.

Document B:
How to update account login credentials.

Document C:
Today's weather forecast.
```

A semantic search system may rank Documents A and B above Document C.

### Keyword Search vs Semantic Search

| Feature | Keyword Search | Semantic Search |
|---|---|---|
| Main approach | Match words or terms | Compare meaning-related representations |
| Exact wording | Often useful | Not always required |
| Synonyms | Depends on search configuration | Can often identify related wording |
| Numerical vectors | Not required | Commonly used |
| Best use | Exact names, IDs, terms | Meaning-based retrieval |

### Hybrid Search

Hybrid search combines lexical retrieval, such as BM25 keyword search, with semantic vector search.

It can be useful when a system must handle both exact terms and natural-language questions.

For example, searching for a specific error code may benefit from keyword matching, while searching for "how do I recover access to my account?" may benefit from semantic retrieval.

---

## 4.12 How Embeddings Work in RAG

RAG uses retrieval to supply relevant external information to a generative language model.

Embeddings commonly support the retrieval stage.

### Document Indexing Stage

This process is usually performed before the user asks a question.

```text
Documents
    |
    v
Extract Text
    |
    v
Split Text into Chunks
    |
    v
Generate Chunk Embeddings
    |
    v
Store Vectors + Text + Metadata
```

### Query Stage

This process happens when a user asks a question.

```text
User Question
    |
    v
Generate Query Embedding
    |
    v
Search Vector Database
    |
    v
Retrieve Relevant Chunks
    |
    v
Build Prompt with Context
    |
    v
Generative LLM
    |
    v
Answer with Source Citations
```

### Example

Suppose the knowledge base contains:

```text
Chunk 1:
Users can reset their password through the account recovery page.

Chunk 2:
The support team responds to technical requests during business hours.

Chunk 3:
The company provides several training programs.
```

User question:

```text
How can I recover my account password?
```

The application generates an embedding for the question and searches the document vectors.

Chunk 1 may be retrieved because it is semantically relevant.

The LLM receives the question and retrieved text and generates an answer.

The application can attach a citation that points to the source document for Chunk 1.

### Key Learning

Embeddings help the retrieval system find potentially relevant information. The LLM uses the retrieved information to generate the answer.

---






## 4.17 Common Mistakes When Working with Embeddings

### Mistake 1: Assuming More Dimensions Always Mean Better Results

A model with more dimensions is not automatically more accurate.

**Solution:** Evaluate retrieval quality using representative questions and documents.

### Mistake 2: Treating Similarity as a Probability

A cosine similarity of 0.8 does not necessarily mean an 80% chance of correctness.

**Solution:** Treat scores as model- and dataset-dependent ranking signals.

### Mistake 3: Embedding Only the User Question

A RAG system must also embed and index document chunks before it can retrieve them through vector search.

**Solution:** Generate embeddings for both the document collection and the user's query.

### Mistake 4: Using Different Models for Documents and Queries

Different embedding models may produce incompatible vector representations.

**Solution:** Use a compatible model and configuration for both sides of the retrieval process.

### Mistake 5: Ignoring Chunking

Embedding an entire large document as one unit may make precise retrieval difficult or exceed the model's input limit.

**Solution:** Split documents into meaningful chunks before generating embeddings.

### Mistake 6: Assuming the Most Similar Chunk Must Be Correct

The most similar document may still be incomplete, outdated, or irrelevant to the specific question.

**Solution:** Evaluate retrieved results and consider reranking, metadata filters, hybrid search, and relevance thresholds where appropriate.

### Mistake 7: Forgetting to Rebuild the Index

Changing the embedding model while keeping vectors from the old model can cause incompatible retrieval behavior.

**Solution:** Regenerate embeddings and rebuild the index when changing models or incompatible embedding configurations.

### Mistake 8: Ignoring Metadata

A vector alone does not provide all the information needed to show the original source.

**Solution:** Store the chunk text and useful metadata, such as the document ID, source URL, title, and chunk ID.

---

## 4.18 How to Evaluate Embedding Retrieval Quality

A good embedding model should retrieve useful passages for your real queries.

Do not choose a model based only on its name, dimension, or one successful example.

### Build a Small Test Dataset

Create several questions and identify the documents that should answer them.

Example:

| Question | Expected relevant document |
|---|---|
| How do I reset my password? | Password recovery guide |
| What is the support team's schedule? | Support hours document |
| Where can I find training materials? | Training resources page |

### Test Your Retrieval System

For each question:

1. Generate the query embedding.
2. Retrieve the top-ranked documents.
3. Check whether the expected relevant document appears.
4. Record its rank.
5. Repeat for all test questions.

### Useful Retrieval Metrics

**Precision@k**

Measures how many of the top `k` retrieved results are relevant.

**Recall@k**

Measures how many of the known relevant documents appear among the top `k` results.

**Mean Reciprocal Rank (MRR)**

Measures how highly the first relevant result is ranked across a set of queries.

### Example

If the correct document appears first for a question, that query has a reciprocal rank of 1.

If it first appears in position 3, its reciprocal rank is 1/3.

These metrics help evaluate retrieval quality before assessing the LLM's generated answers.

### Key Learning

Evaluate embeddings as part of the retrieval system, using representative questions and known relevant documents.

---

## 4.19 Embeddings and Vector Databases

A vector database stores vectors and supports similarity search.

Depending on the system, it can also store text, metadata, and references to source documents.

### Example Data Structure

```json
{
  "id": "chunk_001",
  "text": "Users can reset a forgotten password through account recovery.",
  "embedding": [0.12, -0.08, 0.41],
  "metadata": {
    "source": "account_help.md",
    "page": 1
  }
}
```

The embedding shown is illustrative and shortened. A real vector must have the correct dimension for the chosen model.

### Popular Vector Search Options

- Chroma.
- FAISS.
- Qdrant.
- Milvus.
- Weaviate.
- PostgreSQL with pgvector.

These options differ in deployment, filtering, persistence, scaling, and operational features.

### Typical Workflow

```text
Document Chunks
      |
      v
Embedding Model
      |
      v
Numerical Vectors
      |
      v
Vector Database
      |
      v
Similarity Search
      |
      v
Retrieved Chunks
```

### Important Distinction

An embedding model generates vectors. A vector database stores and searches vectors.

They are separate components that work together.

---

## 4.20 Key Learning Summary

- Embeddings are numerical representations of data.
- Text embeddings help represent aspects of sentence or passage meaning.
- Semantic search uses embeddings to find related content even when wording differs.
- Embedding dimensions determine how many values are present in each vector.
- Cosine similarity compares vector directions.
- Dot product and Euclidean distance are other common comparison measures.
- Sentence embeddings are widely used in RAG retrieval.
- Document chunks are embedded and indexed before user queries arrive.
- User questions are embedded at query time.
- Vector databases search stored embeddings and return relevant content.
- Similarity does not guarantee correctness.
- Retrieval quality should be tested with representative questions and relevant documents.
- In RAG, embeddings support retrieval, while a generative LLM creates the final answer.

**Final takeaway:** Embeddings help a RAG system find relevant information by representing text as numerical vectors. Good embeddings can improve retrieval, but reliable RAG also requires appropriate chunking, indexing, ranking, source tracking, and evaluation.

---

## 4.21 Checklist: What You Should Be Able to Do

- [ ] Explain what embeddings are.
- [ ] Explain why embeddings are useful in RAG.
- [ ] Describe how text is converted into a vector.
- [ ] Explain embedding dimensions.
- [ ] Distinguish word embeddings from sentence embeddings.
- [ ] Explain semantic similarity.
- [ ] Explain cosine similarity.
- [ ] Distinguish cosine similarity, dot product, and Euclidean distance.
- [ ] Generate embeddings using Python.
- [ ] Compare sentence embeddings using cosine similarity.
- [ ] Rank documents for a sample query.
- [ ] Explain how embeddings work with a vector database.
- [ ] Describe the role of embeddings in a RAG pipeline.
- [ ] Explain why similarity scores do not guarantee factual correctness.
