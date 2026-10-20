# Lesson 13: Hybrid Search and Reranking

## 13.1 Learning Objectives

By the end of this lesson, you should understand:

- Dense retrieval using embeddings.
- Sparse retrieval using keywords and BM25.
- The differences between dense and sparse retrieval.
- Why combining dense and sparse retrieval can improve search.
- Reciprocal Rank Fusion (RRF).
- Cross-encoder reranking.
- Metadata filtering for eligible content.
- How to build a hybrid retrieval pipeline in Python.
- How to compare dense-only, keyword-only, and hybrid retrieval on the same questions.
- How to measure retrieval recall and latency in the practical exercise.

## 13.2 Dense Retrieval

Dense retrieval uses embeddings to represent a query and documents as numerical vectors. A vector similarity method then finds documents whose embeddings are close to the query embedding.

For example, suppose a knowledge base contains these documents:

- **D1:** How to reset your account password.
- **D2:** Steps to recover access to your account.
- **D3:** Python programming fundamentals.
- **D4:** How to change your login credentials.

**User query:**

> How can I regain access to my account?

A dense retriever may find D2 relevant even though the document does not contain the exact phrase “regain access.” This is because the query and document can express similar meanings using different words.

### Advantages of Dense Retrieval

1. Understands semantic similarity.
2. Can retrieve relevant documents when the query and document use different wording.
3. Helps with paraphrases and natural-language questions.
4. Can retrieve conceptually related information without requiring exact keyword matches.

### Limitations of Dense Retrieval

1. May overlook exact identifiers, codes, or uncommon terms.
2. Results depend on the embedding model and how well it represents the domain.
3. Semantically similar documents may not contain the specific evidence required.
4. Embedding generation and vector search require computational resources.

Dense retrieval is especially useful when users describe a concept in their own words.

## 13.3 Sparse Retrieval

Sparse retrieval represents documents and queries using terms or features that are mostly zero. Traditional keyword search and BM25 are common examples. Unlike dense retrieval, sparse retrieval does not primarily depend on semantic embedding similarity.

**Query:**

> Error code AUTH-4017

**Document:**

> Troubleshooting error AUTH-4017 during authentication.

A keyword retriever can match the exact error code. A dense retriever may or may not rank that document highly, depending on its embedding model and the surrounding text.

### What Is BM25?

BM25 is a ranking algorithm widely used in information retrieval to estimate how relevant a document is to a query. It is also commonly referred to as **Okapi BM25**.

BM25 considers factors such as:

- **Term frequency (TF):** How often a query term appears in a document, with diminishing returns.
- **Inverse document frequency (IDF):** How informative a term is across the collection.
- **Document length:** How long the document is compared with the collection’s typical document length.

A simplified BM25 expression is:

\[
\operatorname{BM25}(D,Q)=
\sum_{t\in Q}
\operatorname{IDF}(t)
\frac{f(t,D)(k_1+1)}
{f(t,D)+k_1\left(1-b+b\frac{|D|}{\operatorname{avgdl}}\right)}
\]

Where:

- \(D\) is a document.
- \(Q\) is a query.
- \(t\) is a query term.
- \(f(t,D)\) is the frequency of term \(t\) in document \(D\).
- \(|D|\) is the document length.
- \(\operatorname{avgdl}\) is the average document length.
- \(k_1\) controls term-frequency saturation.
- \(b\) controls document-length normalization.
- \(\operatorname{IDF}(t)\) measures how informative the term is across the collection.

You do not need to memorize the formula immediately. Focus on understanding how BM25 ranks documents.

### Advantages of Sparse Retrieval

1. Strong for exact terms, product codes, names, and identifiers.
2. Easy to inspect why a document matched a query.
3. Does not require an embedding model.
4. Useful when exact wording is important.

### Limitations of Sparse Retrieval

1. Can miss relevant documents that use different wording.
2. May struggle with synonyms and paraphrases.
3. A keyword match does not necessarily mean the document is relevant.
4. Performance depends on the quality of the text representation and ranking configuration.

BM25 is a strong baseline for keyword-based document retrieval.

## 13.4 Dense Retrieval vs. Sparse Retrieval

| Feature | Dense retrieval | Sparse retrieval |
|---|---|---|
| Representation | Dense numerical vectors | Sparse term-based representations |
| Typical method | Embedding similarity | BM25 or keyword search |
| Semantic matching | Usually stronger | Usually weaker |
| Exact identifier matching | May be inconsistent | Often strong |
| Synonyms and paraphrases | Often strong | May miss them |
| Explainability | Similarity scores can be difficult to interpret | Matched terms are easier to inspect |
| Main dependency | Embedding model | Tokenization and term-ranking method |
| Example strength | “Recover account access” matches “Restore account login” | `AUTH-4017` matches `AUTH-4017` |

Neither approach is best for every query. Dense and sparse retrieval can return complementary results. Combining them is the main idea behind hybrid search.

## 13.5 What Is Hybrid Search?

Hybrid search combines results from multiple retrieval methods, commonly:

- **Dense retrieval:** Finds semantically similar content.
- **Sparse retrieval:** Finds content using matching terms.

Each retriever produces its own ranked list of candidate documents. Hybrid search combines those lists into a single ranking.

**User query:**

> How do I fix AUTH-4017 when logging in?

**Possible dense retrieval results:**

| Rank | Document |
|---:|---|
| 1 | D2 — Troubleshooting login failures |
| 2 | D3 — Recovering account access |
| 3 | D1 — Authentication error reference |

**Possible sparse retrieval results:**

| Rank | Document |
|---:|---|
| 1 | D1 — Authentication error AUTH-4017 |
| 2 | D4 — AUTH-4017 troubleshooting guide |
| 3 | D2 — Troubleshooting login failures |

Dense retrieval finds relevant meaning. Sparse retrieval finds the exact error code. Hybrid search can combine both sets so that useful results from either approach are retained.

### Hybrid Search Architecture

```text
                         User Query
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
          Dense Retriever         Sparse Retriever
          Embedding Search        BM25 / Keywords
                 |                       |
                 v                       v
           Ranked List A           Ranked List B
                 |                       |
                 +-----------+-----------+
                             |
                             v
                 Reciprocal Rank Fusion
                             |
                             v
                 Combined Candidate List
                             |
                             v
                    Metadata Filtering
                             |
                             v
                 Cross-Encoder Reranker
                             |
                             v
                  Final Ranked Results
```

This is one possible architecture. Some systems apply metadata filters inside each retriever before fusion, while others filter candidates after fusion. Filtering before retrieval is often more efficient when the retrieval system supports it. Filtering after fusion can act as an additional safety check.

## 13.6 Why Combine Dense and Sparse Retrieval?

Imagine that your knowledge base contains these documents:

- **D1:** The account recovery process restores access to an account.
- **D2:** AUTH-4017 indicates a login authentication error.
- **D3:** Resetting a forgotten password.
- **D4:** Python lists and dictionaries.

**User query:**

> How can I fix AUTH-4017 and recover my account?

The query has two important parts:

1. `AUTH-4017` is an exact identifier.
2. “Recover my account” describes a broader concept.

Sparse retrieval may be particularly useful for the identifier. Dense retrieval may find relevant recovery instructions expressed in different words. Hybrid retrieval helps by combining these complementary signals.

### When Hybrid Search Is Useful

- Enterprise knowledge bases containing technical identifiers.
- Customer-support systems containing error codes.
- Documentation with product names, versions, and configuration keys.
- Search over policies where users paraphrase official wording.
- Knowledge bases containing both exact terminology and natural-language explanations.

### When Hybrid Search May Not Help Much

- A collection where one retriever already performs well for almost every query.
- Very small collections with simple, exact-match questions.
- Systems where retrieval quality is limited by missing or outdated source content.
- Systems where the two retrievers return almost identical results.

Hybrid search is a technique to improve candidate discovery, not a guarantee that every query will improve.

## 13.7 Combining Rankings with Reciprocal Rank Fusion (RRF)

Dense and sparse retrievers usually produce different kinds of scores.

For example:

**Dense similarity scores:**

- D1 = 0.87
- D2 = 0.81

**BM25 scores:**

- D3 = 8.7
- D1 = 5.2

These scores are not directly comparable. Dense similarity might be bounded within a particular range, while BM25 scores depend on the query and corpus. One approach is to combine the ranked lists rather than directly add their raw scores.

Reciprocal Rank Fusion (RRF) is a ranking method that combines multiple ranked lists using the rank of each document.

The formula is:

\[
\operatorname{RRF}(d)=
\sum_{r \in R}
\frac{1}{k+\operatorname{rank}_r(d)}
\]

Where:

- \(d\) is a document.
- \(R\) is the set of ranked result lists.
- \(\operatorname{rank}_r(d)\) is the document’s position in list \(r\), starting at 1.
- \(k\) is a constant that reduces the impact of differences between ranks.

A common example uses \(k=60\), although the best value depends on the application.

### Example of RRF

Suppose two retrievers return the following rankings.

**Dense ranking:**

1. D1
2. D2
3. D3

**Sparse ranking:**

1. D3
2. D1
3. D4

Using \(k=60\):

| Document | Dense rank | Sparse rank | RRF score |
|---|---:|---:|---|
| D1 | 1 | 2 | \(1/61 + 1/62\) |
| D2 | 2 | — | \(1/62\) |
| D3 | 3 | 1 | \(1/63 + 1/61\) |
| D4 | — | 3 | \(1/63\) |

The resulting order is:

1. D1
2. D3
3. D2
4. D4

D1 ranks highly in both lists. D3 receives a strong combined score because it ranks first in sparse retrieval and third in dense retrieval. A document missing from one list contributes zero from that list.

### Why Use RRF?

- It avoids directly comparing incompatible raw scores.
- It rewards documents that rank highly across multiple retrieval methods.
- It is straightforward to implement.
- It works with ranked lists from more than two retrievers.

### Limitations of RRF

- It uses rank positions rather than the full magnitude of the original scores.
- It cannot make an irrelevant document relevant.
- Its output depends on the candidate lists and the selected \(k\).
- It does not independently verify that a result supports a query.

RRF is a ranking-combination method. It does not understand the meaning of the query itself.

## 13.9 Candidate Retrieval and Reranking Are Different

Hybrid retrieval produces a candidate list. Reranking then reorders those candidates using a more targeted relevance model.

**Query:**

> How do I resolve AUTH-4017?

**Hybrid retrieval results:**

1. General login help
2. AUTH-4017 troubleshooting
3. Password reset instructions
4. Account security overview

**After reranking:**

1. AUTH-4017 troubleshooting
2. General login help
3. Password reset instructions
4. Account security overview

The candidate list already contains the correct document. The reranker moves it to the top.

Reranking usually cannot recover a document that was never retrieved into the candidate set. This is why the initial retrieval stage must return a sufficiently broad set of candidates.

## 13.10 Cross-Encoder Reranking

A cross-encoder is a model that takes a query and a document together and estimates their relevance to each other.

For example, given the query:

> How can I recover a locked account?

A cross-encoder scores candidate pairs such as:

**Pair 1**

- Query: How can I recover a locked account?
- Document: Follow these steps to restore access to your account.

**Pair 2**

- Query: How can I recover a locked account?
- Document: Python is a programming language.

The first pair should receive a higher relevance score than the second. The cross-encoder evaluates the query and document jointly, allowing it to model interactions between their words and context.

### How Does a Cross-Encoder Work?

1. Receive the query and one candidate document.
2. Combine the query and document into a model input.
3. Process the combined input through the model.
4. Produce a relevance score.
5. Repeat for the other candidates.
6. Sort candidates by their scores.

The score is usually a ranking signal, not a calibrated probability that the document is correct.

### Bi-Encoder vs. Cross-Encoder

A bi-encoder is commonly used for dense retrieval. It encodes the query and each document separately. A cross-encoder processes each query-document pair together.

| Feature | Bi-encoder | Cross-encoder |
|---|---|---|
| Input | Query and document encoded separately | Query and document processed together |
| Main purpose | Retrieve candidates efficiently | Rerank candidates for relevance |
| Document vectors | Can be precomputed | Usually does not use precomputed document embeddings for pair scoring |
| Search over large collections | Efficient | Expensive to apply to every document |
| Pair-specific interaction | Limited during initial vector search | Modeled directly |
| Common pipeline position | Initial retrieval | After candidate retrieval |

### Why Not Use a Cross-Encoder for Every Document?

Suppose your collection has 100,000 chunks. Scoring every chunk against each query with a cross-encoder can be expensive.

Instead, a typical pipeline works like this:

1. Retrieve a manageable candidate set using dense search and/or BM25.
2. Combine the candidates with RRF.
3. Score the candidates with a cross-encoder.
4. Return the highest-ranked results.

This limits the more expensive model to a smaller set of documents.

### Benefits of Reranking

- Improves the ordering of retrieved candidates.
- Can distinguish documents with similar wording but different relevance.
- Can place the most useful evidence near the top of the final list.
- Can combine well with dense-only or hybrid retrieval.

### Limitations of Reranking

- Adds model inference latency.
- Requires scoring each candidate.
- Cannot normally recover relevant documents missing from the candidate list.
- Can be affected by model domain mismatch and input-length limits.
- A high score does not guarantee factual correctness.

## 13.11 Implement Cross-Encoder Reranking in Python

For this exercise, use a pretrained cross-encoder from the `sentence-transformers` library.

Install the dependency in your project’s active virtual environment:

```bash
python -m pip install sentence-transformers
```

## 13.12 Metadata Filtering in Hybrid Search

Metadata filtering restricts results using attributes associated with documents or chunks.

Example metadata:

```json
{
  "document_id": "doc_001",
  "source_type": "approved_document",
  "department": "support",
  "language": "en",
  "status": "published"
}
```

Suppose a knowledge base contains:

| Document | Department | Status |
|---|---|---|
| D1 | Support | Published |
| D2 | HR | Published |
| D3 | Support | Draft |
| D4 | Support | Published |

If a user is allowed to retrieve only published support documents, D2 and D3 must be excluded.

A metadata filter could require:

```text
department = support
AND
status = published
```

Only D1 and D4 would be eligible.

### Why Metadata Filtering Matters

- Removes content that is not relevant to the requested category.
- Restricts retrieval to the appropriate department, language, or document type.
- Helps enforce document eligibility and access policies.
- Prevents draft or archived content from appearing when it should not be used.

### Filtering Before or After Retrieval

- **Before retrieval:** Apply supported metadata conditions within each retriever. This avoids spending ranking effort on ineligible documents and can reduce computation.
- **After retrieval:** Check the fused candidates and remove ineligible results before reranking or returning them. This can serve as a final eligibility check.

A robust system may use both.

### Important Security Rule

Do not rely only on filtering the final list if unauthorized documents could already enter downstream processing. Apply access-control restrictions as early as possible, and verify eligibility again before returning results.

Metadata filters also need consistent metadata values. For example, `published`, `Published`, and `PUBLISHED` may behave differently depending on the database and filtering implementation.

## 13.14 Putting the Components Together

A practical hybrid pipeline combines the techniques in the following order:

1. Apply eligibility constraints that the retrievers support.
2. Retrieve candidates using dense search.
3. Retrieve candidates using BM25.
4. Fuse the rankings using RRF.
5. Apply a final eligibility check.
6. Rerank the eligible candidates using a cross-encoder.
7. Select the highest-ranked results for the next stage of the application.

### Hybrid Retrieval Pipeline

```text
                         Query
                           |
                 +---------+---------+
                 |                   |
                 v                   v
           Dense search          BM25 search
                 |                   |
                 +---------+---------+
                           |
                           v
                      RRF fusion
                           |
                           v
                  Eligibility check
                           |
                           v
                 Cross-encoder reranking
                           |
                           v
                    Final candidates
```

The order can vary. For example, some implementations rerank the fused candidates before applying a final metadata check. The important requirement is that unauthorized or otherwise ineligible documents are never returned.

### Important Parameters

| Parameter | Meaning |
|---|---|
| `dense_top_k` | Number of candidates requested from dense retrieval |
| `bm25_top_k` | Number of candidates requested from BM25 |
| `rrf_k` | Constant used in Reciprocal Rank Fusion |
| `rerank_top_n` | Number of candidates scored by the cross-encoder |
| `final_top_k` | Number of results returned after reranking |
| Metadata conditions | Eligibility rules applied to documents |

These parameters interact. Retrieving more candidates may improve the chance of finding useful evidence, but it can also increase processing time and reranking cost.

## 13.17 Common Problems and Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'rank_bm25'`

Install the package in the active virtual environment:

```bash
python -m pip install rank-bm25
```

### Problem: `ModuleNotFoundError: No module named 'sentence_transformers'`

Install the package in the active virtual environment:

```bash
python -m pip install sentence-transformers
```

### Problem: Model Download Fails

The pretrained model may need internet access on first use. Check network access and retry. Once the model is downloaded and cached, it may be possible to run it offline.

### Problem: The Exact Error Code Is Not Ranked Highly

Check that the query and document contain the identifier in a form that the tokenizer preserves. Also inspect the candidate list returned by BM25 before changing the fusion method.

### Problem: Hybrid Results Contain Duplicates

Use the same stable document or chunk IDs in both retrieval lists. RRF merges matching IDs; it cannot recognize that two different IDs refer to the same content.

### Problem: A Draft Document Appears in the Results

Check the metadata filter in both retrieval paths and the final eligibility check. Do not rely on reranking to exclude drafts or unauthorized documents.

### Problem: Reranking Is Slow

Reduce the number of candidates sent to the cross-encoder, measure model inference separately, and reuse the loaded model instead of reloading it for each query.

### Problem: The Reranker Does Not Return a Relevant Document

Inspect the candidates from hybrid retrieval first. If the document is missing from that candidate set, improve the initial retrieval stage; reranking cannot normally recover it.

## 13.18 Best Practices

1. Use dense retrieval when semantic similarity matters.
2. Use BM25 when exact terms, identifiers, or keywords matter.
3. Consider hybrid retrieval when your query types benefit from both approaches.
4. Use RRF when combining rankings whose raw scores are not directly comparable.
5. Use a cross-encoder to refine a manageable candidate set.
6. Apply metadata and access-control restrictions as early as possible.
7. Keep document IDs consistent across all retrieval stages.
8. Measure retrieval latency and inspect candidate rankings on representative questions.
9. Treat reranker scores as ranking signals, not proof of factual correctness.
10. Do not assume hybrid retrieval or reranking always improves results; their usefulness depends on your documents, queries, and configuration.

## 13.19 Lesson Summary

- **Dense retrieval:** Uses embeddings to find semantically similar content.
- **Sparse retrieval:** Uses terms and ranking methods such as BM25 to find keyword matches.
- **Hybrid search:** Combines dense and sparse retrieval results.
- **RRF:** Combines ranked lists using reciprocal rank contributions.
- **Cross-encoder reranking:** Scores query-document pairs to refine the candidate order.
- **Metadata filtering:** Excludes documents that do not satisfy eligibility conditions.

---

**Note about section numbering:** The source lesson skips sections 13.8, 13.13, 13.15, and 13.16. Those sections were not present in the supplied text, so they have not been invented here.
