
# Lesson 10: Retrieval and Search in RAG



## 10.1 What Is Retrieval?

Retrieval is the process of finding document chunks that are relevant to a user's question.

When a user asks a question, the retrieval component searches the indexed documents and selects the most relevant chunks.

For example, suppose the document collection contains these chunks:

**Chunk 1**
"Retrieval-Augmented Generation uses external documents to provide relevant context to a language model."

**Chunk 2**
"Embeddings represent text as numerical vectors."

**Chunk 3**
"Python is a general-purpose programming language."

User question:

"How does RAG find information from documents?"

The retrieval system should return Chunk 1 because its meaning is most closely related to the question.

### Why Is Retrieval Important?

The language model can only use the retrieved evidence that is made available to it.

If the correct information exists in the database but retrieval selects unrelated chunks, the model may produce an incomplete or incorrect answer.

Good retrieval helps the application:

- Find relevant evidence.
- Reduce irrelevant context.
- Avoid searching the entire document collection manually.
- Provide useful information to the generation component.
- Improve the relevance of answers.

---

## 10.2 Retrieval Pipeline

A basic vector retrieval pipeline works as follows:

1. Receive a user question.
2. Convert the question into an embedding.
3. Search the vector database using the query embedding.
4. Compare the query with stored document embeddings.
5. Rank the matching chunks.
6. Select the top-k results.
7. Optionally apply a similarity threshold or metadata filter.
8. Return the selected chunks and their metadata.

The stored document embeddings are normally created during the indexing process. They do not need to be regenerated for every user question.

### Architecture Diagram

User Question
      |
      v
Query Embedding
      |
      v
Vector Database Search
      |
      v
Similarity / Distance Calculation
      |
      v
Rank Retrieved Chunks
      |
      v
Apply Top-k and Optional Filters
      |
      v
Return Relevant Chunks
      |
      v
Available for the Next RAG Stage

### Example

Question:
"What is semantic search?"

The system converts the question into a numerical vector and searches for stored vectors representing related content.

Possible results:

| Rank | Chunk | Relevance |
|---|---|---|
| 1 | Semantic search finds text based on meaning. | High |
| 2 | Embeddings represent text numerically. | High |
| 3 | Python supports object-oriented programming. | Low |

The actual ranking depends on the embedding model, distance metric, document content, and search configuration.

---

## 10.3 Query Embeddings

A query embedding is a numerical representation of the user's question.

For example:

Question:
"How does semantic search work?"

Illustrative embedding:

[0.12, -0.08, 0.41, 0.27, ...]

These values are only an example. Real embeddings usually contain many more dimensions.

The vector database compares the query embedding with the stored document embeddings.

### Why Use Query Embeddings?

Text can express the same idea in different ways.

For example:

- "How do I reset my password?"
- "I forgot my login credentials. How can I access my account?"
- "What should I do if I cannot remember my password?"

An embedding model may represent these questions as semantically related, even though they use different words.

This enables semantic search to find conceptually related content rather than relying only on identical words.

### Important Rule

Use a compatible embedding model and configuration for document embeddings and query embeddings.

If document vectors were generated with one embedding model, switching to an unrelated model for queries can make the search results unreliable.

---

## 10.4 Similarity and Distance

A vector database needs a mathematical method to compare the query vector with document vectors.

Common measures include:

1. Cosine similarity
2. Euclidean distance
3. Dot product

These measures do not all use the same score direction or range.

### 10.4.1 Cosine Similarity

Cosine similarity measures the angle between two vectors.

A higher cosine similarity generally indicates that two vectors point in a more similar direction.

For normalized vectors, cosine similarity is commonly between -1 and 1.

Interpretation:

- Closer to 1: vectors point in similar directions.
- Around 0: vectors are approximately orthogonal.
- Closer to -1: vectors point in opposite directions.

These are geometric interpretations, not guaranteed measures of human-perceived relevance.

### 10.4.2 Euclidean Distance

Euclidean distance measures the straight-line distance between two vectors.

A smaller distance means the vectors are closer under this metric.

For example:

- Distance 0.15: relatively close.
- Distance 0.75: farther apart.

These numbers are illustrative. Their meaning depends on the embedding model and data.

### 10.4.3 Dot Product

The dot product multiplies corresponding vector dimensions and sums the results.

Depending on the model and whether vectors are normalized, a higher dot product may indicate greater similarity.

Unlike cosine similarity, raw dot-product scores can depend on vector magnitudes.

### Comparison

| Measure | Better match usually means | Important detail |
|---|---|---|
| Cosine similarity | Higher score | Measures vector direction |
| Euclidean distance | Lower score | Measures vector distance |
| Dot product | Higher score | Can depend on vector magnitude |

### Important: Similarity Is Not the Same as Distance

A similarity score and a distance score must not be interpreted in the same way.

For example, a score of 0.2 could mean a low similarity or a small distance, depending on the metric and library.

Always check the vector database documentation to understand what the returned score means.

---

## 10.5 Understanding Search Results

A vector search commonly returns:

- Document or chunk IDs
- Text content
- Metadata
- Similarity or distance scores
- Result rankings

Example:

| Rank | ID | Distance | Content |
|---|---|---:|---|
| 1 | chunk_12 | 0.18 | Semantic search compares the meaning of text. |
| 2 | chunk_05 | 0.31 | Embeddings represent text as vectors. |
| 3 | chunk_27 | 0.74 | Python supports functions and classes. |

This example assumes that lower distance is better.

The numbers are illustrative and should not be treated as universal relevance cutoffs.

### What Should You Inspect?

When checking a retrieval result, ask:

1. Is the retrieved content relevant to the question?
2. Does it contain evidence that can answer the question?
3. Are the results ranked sensibly?
4. Are duplicate or nearly identical chunks appearing?
5. Is important evidence missing?
6. Is unrelated content being returned?
7. Does the metadata identify the source document?

A result with a good-looking score is not necessarily useful. Inspect the actual text.

---

## 10.6 Top-k Retrieval

Top-k is the number of results selected from a search.

For example, if `top_k = 3`, the system requests the three best-matching results, subject to the database's available results and any filters.

### Example

Question:
"What are embeddings used for?"

Suppose the ranked candidates are:

1. chunk_04 — Embeddings convert text into numerical vectors.
2. chunk_09 — Vector search compares embedding representations.
3. chunk_15 — Similarity measures compare vectors.
4. chunk_21 — Python variables store values.
5. chunk_30 — A web server handles requests.

If `top_k = 3`, the first three chunks are selected.

### What Happens When Top-k Changes?

**Small top-k**

Advantages:
- Returns less content.
- May reduce irrelevant results.
- Uses less context in later processing.

Limitations:
- May miss useful supporting evidence.
- May be insufficient when the answer requires several chunks.

**Large top-k**

Advantages:
- Retrieves more possible evidence.
- Can help when information is spread across multiple chunks.

Limitations:
- May include irrelevant content.
- May return redundant chunks.
- Increases the amount of context passed to later stages.

### Choosing Top-k

There is no single best value for every dataset.

Start with a small value, such as 3 or 5, inspect the results, and adjust based on the needs of your application.

For this lesson, compare values such as 3, 5, and 10 to understand how the result set changes.

---

## 10.7 Similarity Threshold

A similarity threshold is a rule used to exclude results that do not meet a chosen relevance-score condition.

For example, an application might accept results only when their cosine similarity is above a configured threshold.

The exact condition depends on the metric:

- Similarity score: often keep results above a threshold.
- Distance score: often keep results below a threshold.

### Example: Cosine Similarity

Suppose an application uses a hypothetical minimum cosine similarity of 0.65.

| Chunk | Similarity | Decision |
|---|---:|---|
| chunk_01 | 0.86 | Keep |
| chunk_02 | 0.72 | Keep |
| chunk_03 | 0.51 | Exclude |
| chunk_04 | 0.29 | Exclude |

These scores are illustrative.

### Why Is Threshold Selection Important?

If the threshold is too strict:

- Relevant chunks may be excluded.
- Questions may receive no useful context.

If the threshold is too permissive:

- Weakly related chunks may be returned.
- Unrelated information may enter the result set.

### How to Choose a Threshold

1. Collect representative questions.
2. Inspect their retrieved results and scores.
3. Identify relevant and irrelevant matches.
4. Try different threshold values.
5. Check whether relevant evidence is being excluded.
6. Choose a value suitable for the particular model, metric, and dataset.

Do not copy a threshold from another project without testing it.

### No-Result Handling

A retrieval system should handle cases where no results remain after filtering.

Possible application behaviors include:

- Return an empty result list.
- Record a diagnostic message.
- Ask the user to rephrase the question.
- Let the next stage follow an appropriate no-evidence policy.

Do not assume that the database will always find an answer.

---

## 10.8 Metadata Filtering

Metadata filtering restricts search results based on properties associated with documents or chunks.

Examples of metadata fields:

- `topic`
- `source`
- `document_type`
- `language`
- `department`
- `year`
- `access_level`

Metadata filtering is useful when only a specific subset of the collection is eligible for a query.

### Example

Suppose the database contains these documents:

| ID | Topic | Content |
|---|---|---|
| doc_01 | rag | Introduction to retrieval |
| doc_02 | embeddings | How embeddings work |
| doc_03 | rag | Selecting relevant chunks |
| doc_04 | python | Python programming basics |

Question:
"How does retrieval work?"

If the search should be limited to the `rag` topic, the filter restricts the candidate set to documents tagged `rag`.

### ChromaDB Example

```python
results = collection.query(
    query_texts=["How does retrieval work?"],
    n_results=3,
    where={"topic": "rag"},
)

print(results["ids"])
print(results["documents"])
print(results["metadatas"])
print(results["distances"])
```

This example assumes that the collection already contains documents with a `topic` metadata field.

### Filtering by Another Field

For example, a collection might contain a `document_type` field.

```python
results = collection.query(
    query_texts=["Explain embeddings"],
    n_results=3,
    where={"document_type": "tutorial"},
)
```

This returns matching candidates that also satisfy the metadata condition.

### Combining Metadata Conditions

ChromaDB supports compound metadata filters.

Example:

```python
results = collection.query(
    query_texts=["Explain retrieval"],
    n_results=5,
    where={
        "$and": [
            {"topic": "rag"},
            {"language": "en"},
        ]
    },
)
```

This example assumes the records have both `topic` and `language` metadata fields.

### Important Considerations

- Metadata filters use the values stored in the database.
- A filter cannot find records that do not satisfy the specified condition.
- Incorrect metadata can cause relevant chunks to be excluded.
- Metadata filtering is not the same as semantic relevance ranking.
- Access restrictions must be enforced using trusted application logic, not merely user-supplied filter values.

---

## 10.9 Semantic Search Versus Exact Keyword Search

Semantic search compares the meaning represented by embeddings.

Exact keyword search looks for matching terms or phrases.

For this lesson, the focus is on understanding the difference between these basic search behaviors. Combining keyword search with vector search is covered in the upcoming hybrid-search lesson.

### Example

Stored text:

"The application allows users to recover access to their accounts."

Query:

"How can I regain access to my account?"

An exact keyword search may struggle because the query and document use different words.

A semantic search system may retrieve the text because the meanings are related.

### When Semantic Search Helps

- Users phrase questions differently from the source documents.
- Synonyms are used.
- Questions express an idea rather than copying source wording.
- The same concept appears in different language patterns.

### Semantic Search Limitations

Semantic search can still fail when:

- The embedding model does not represent the domain well.
- The question is ambiguous.
- Important details are buried in a long or noisy chunk.
- Two topics are semantically similar but factually different.
- The expected answer depends on an exact identifier or unusual term.
- The correct document is missing from the indexed collection.

Semantic similarity is not proof that a chunk contains the correct answer.

---

## 10.10 Searching Across Multiple Documents

Some questions require evidence from more than one document.

Example collection:

**Document A**
"ChromaDB stores document embeddings and supports similarity search."

**Document B**
"An embedding model converts text into numerical vectors."

**Document C**
"Python is used to implement many data-processing applications."

Question:

"How do embeddings and ChromaDB work together in a retrieval system?"

A useful result set may need both Document A and Document B.

The first document explains vector storage and search. The second explains how the vectors are created.

### Why Can Multi-Document Retrieval Be Difficult?

- The answer is distributed across different chunks.
- Each chunk contains only part of the required information.
- One relevant chunk ranks lower than unrelated content.
- A top-k value that is too small excludes supporting evidence.
- Metadata filters accidentally exclude one of the relevant documents.

### Practical Approach

1. Write a question that requires information from at least two documents.
2. Search the collection.
3. Inspect the returned IDs and content.
4. Check whether all necessary pieces of evidence are present.
5. Increase top-k temporarily if evidence appears to be missing.
6. Check metadata restrictions and scores.
7. Record which evidence was retrieved and which was missed.

Do not assume that retrieving one relevant chunk means the entire question is answerable.

---

## 10.11 Questions That Have No Answer in the Corpus

A retrieval system may return results even when the collection does not contain the answer.

For example, the database contains only documents about RAG, embeddings, and vector databases.

Question:

"What is the capital of Japan?"

The database may return the nearest available chunks, but those chunks may not contain the answer.

### Why Does This Happen?

Vector search usually ranks available candidates by their similarity or distance. Ranking the best available candidates does not guarantee that any candidate is genuinely relevant.

### What Should You Check?

- Does the corpus contain information about the requested subject?
- Are the top results related to the question?
- Do the retrieved chunks provide direct evidence?
- Does the threshold remove weak matches?
- Did a metadata filter exclude relevant content?

### Important Lesson

A non-empty result list does not guarantee that the answer exists in the corpus.

Likewise, an empty result list does not always prove that the corpus lacks the answer. A strict threshold or restrictive metadata filter may have removed useful chunks.

---

## 10.12 Inspecting Retrieval Results in Python

When debugging search behavior, inspect the actual retrieved IDs, documents, metadata, and distances.

For a ChromaDB query:

```python
results = collection.query(
    query_texts=["What is semantic search?"],
    n_results=5,
)

ids = results["ids"][0]
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

for rank, (doc_id, document, metadata, distance) in enumerate(
    zip(ids, documents, metadatas, distances),
    start=1,
):
    print(f"\nRank: {rank}")
    print(f"ID: {doc_id}")
    print(f"Distance: {distance}")
    print(f"Metadata: {metadata}")
    print(f"Content: {document}")
```

### Understanding the Output

- `ids`: identifiers for the returned records.
- `documents`: text stored for the returned records.
- `metadatas`: stored metadata for each record.
- `distances`: distance values returned by the configured collection.

The example assumes the collection has these fields available. If the collection was configured differently, inspect the available result fields and database configuration.

For this ChromaDB example, a lower distance generally means a closer match under the collection's configured distance metric.

Do not interpret a distance as a probability that the result is correct.

---

## 10.17 Common Retrieval Problems and Troubleshooting

### Problem 1: Relevant Information Is Not Retrieved

Possible causes:

- The relevant document is not in the collection.
- The query is ambiguous.
- The embedding model does not represent the query well.
- The stored and query embeddings are incompatible.
- The relevant chunk ranks below top-k.
- A metadata filter excludes the document.

What to do:

1. Verify that the source document exists in the collection.
2. Search using a simpler version of the question.
3. Try a paraphrase.
4. Inspect more results.
5. Check the metadata and embedding configuration.

### Problem 2: Too Many Irrelevant Results

Possible causes:

- Top-k is too large for the query.
- The question is too broad.
- The corpus contains similar but unrelated content.
- The similarity or distance metric is being interpreted incorrectly.

What to do:

1. Inspect the result text.
2. Compare different top-k values.
3. Check whether a calibrated threshold would help.
4. Narrow the question if its intent is unclear.

### Problem 3: Search Returns the Wrong Topic

Possible causes:

- Several topics use similar language.
- The query is ambiguous.
- Relevant metadata is missing or incorrect.
- The embedding model does not distinguish the concepts well.

What to do:

1. Inspect the top-ranked content.
2. Add specific terms to the test query.
3. Check metadata values.
4. Compare the results for different phrasings.

### Problem 4: No Results Are Returned

Possible causes:

- No records satisfy the metadata filter.
- The threshold excludes all candidates.
- The collection is empty.
- The requested number of results is invalid for the collection or query configuration.

What to do:

1. Verify that the collection contains records.
2. Run a query without the filter.
3. Check threshold and distance logic.
4. Confirm that the requested result count is valid.

### Problem 5: The Correct Document Exists but Ranks Too Low

Possible causes:

- Other documents are more similar to the query.
- The question is too general.
- The embedding model does not capture the relevant distinction.
- The collection contains duplicate or overlapping content.

What to do:

1. Inspect a larger result set.
2. Compare several query phrasings.
3. Verify that the intended document is indexed correctly.
4. Record which chunks appear before the correct evidence.

Hybrid search and reranking are separate techniques that can be studied in the upcoming lesson.

---

## 10.18 Retrieval Best Practices

Follow these principles when implementing retrieval:

1. Use compatible document and query embedding configurations.
2. Inspect retrieved text, not just scores.
3. Choose top-k based on observed requirements.
4. Calibrate thresholds instead of guessing.
5. Use metadata filters only when their conditions are appropriate.
6. Handle empty and weak result sets explicitly.
7. Test exact questions and paraphrased questions.
8. Test questions that need evidence from multiple documents.
9. Include questions that cannot be answered from the corpus.
10. Keep a record of retrieval behavior during development.
11. Distinguish ranking quality from factual correctness.
12. Diagnose retrieval problems before changing later stages of the application.

---

## 10.19 Key Takeaways

- Retrieval finds candidate chunks relevant to a query.
- Query embeddings let vector databases compare questions with stored document vectors.
- Similarity and distance scores have different interpretations.
- Top-k controls how many results are requested.
- Thresholds can exclude weak matches but may also remove relevant evidence.
- Metadata filters restrict the eligible records.
- Semantic search can handle different phrasings, but it is not perfect.
- A non-empty result list does not prove that the corpus contains the answer.
- Multi-document questions may require several supporting chunks.
- Inspecting IDs, content, metadata, and scores helps diagnose search behavior.
- If retrieval fails to supply the required evidence, the next stage cannot reliably use that missing evidence.

**Final lesson:** Before investigating why a RAG application produces an incorrect answer, check whether retrieval returned the right evidence in the first place.

---

