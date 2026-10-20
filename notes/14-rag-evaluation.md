
# Lesson 14: RAG Evaluation

## 14.1 What Is RAG Evaluation?

RAG evaluation is the process of measuring how well a Retrieval-Augmented Generation (RAG) system retrieves relevant information and generates accurate, grounded answers.

A RAG system has two major responsibilities:

1. Retrieve the correct information from a knowledge base.
2. Generate an answer based on the retrieved information.

Evaluation helps us determine whether both steps work correctly.

For example, if a user asks:

"What is the password recovery procedure?"

The RAG system should:
- Retrieve the document containing the password recovery procedure.
- Provide an answer supported by that document.
- Cite the correct source.
- Avoid inventing information.
- Respond within an acceptable time.

A fluent answer is not necessarily a correct answer. RAG evaluation checks the quality of the evidence, the generated answer, and the overall system behavior.

---

## 14.2 Why Is RAG Evaluation Important?

RAG evaluation is important because a system can fail at multiple stages.

Common problems include:

- Retrieving irrelevant documents.
- Missing the document containing the correct answer.
- Generating an incorrect answer from relevant context.
- Adding information that is not present in the retrieved documents.
- Providing incorrect or unsupported citations.
- Taking too long to generate a response.
- Answering questions when sufficient evidence is unavailable.

Evaluation helps identify these problems before deploying a RAG application to real users.

### Benefits

- Improves retrieval quality.
- Improves answer correctness.
- Reduces hallucinations.
- Improves citation reliability.
- Measures response speed.
- Helps compare embedding models and retrieval strategies.
- Helps identify regressions after code or configuration changes.
- Supports production monitoring and continuous improvement.

---

## 14.3 Where Does Evaluation Fit in the RAG Pipeline?

A typical RAG pipeline looks like this:

```text
User Question
     |
     v
Query Processing
     |
     v
Document Retrieval
     |
     v
Retrieved Context
     |
     v
Prompt Construction
     |
     v
LLM Generation
     |
     v
Generated Answer
     |
     v
Citation and Response Formatting
     |
     v
Final Answer
```

Evaluation can be performed at different stages.

### Retrieval evaluation

Checks whether the retriever finds the expected evidence.

### Generation evaluation

Checks whether the generated answer is correct and supported by the context.

### End-to-end evaluation

Checks the complete system, including retrieval, answer generation, citations, latency, and failure handling.

---

## 14.4 Main Dimensions of RAG Evaluation

The following dimensions help evaluate a RAG system comprehensively.

| Dimension | What it measures |
|---|---|
| Retrieval Recall | Whether expected evidence was retrieved |
| Context Precision | How much retrieved context is relevant |
| Answer Correctness | Whether the answer matches the expected answer |
| Faithfulness | Whether answer claims are supported by context |
| Citation Accuracy | Whether cited sources support the claims |
| Latency | How long retrieval and generation take |
| Failure Handling | Whether the system responds appropriately when evidence is insufficient |

Each metric measures a different aspect of quality. A system may perform well on one metric and poorly on another.

For example, retrieval may find the correct document, but the LLM may still generate an incorrect answer.

---

## 14.5 Building an Evaluation Dataset

An evaluation dataset contains questions, expected answers, expected evidence, and labels describing the type of question.

It acts as a fixed test set for measuring RAG performance.

### Example evaluation record

```json
{
  "question": "What does the document say about password recovery?",
  "expected_answer": "The documented recovery procedure.",
  "expected_source_ids": ["doc-001"],
  "category": "answerable"
}
```

### Explanation of each field

**question**

The question sent to the RAG system.

**expected_answer**

The reference answer that describes the correct information.

**expected_source_ids**

The IDs of documents expected to contain evidence supporting the answer.

A question may have multiple valid supporting sources.

**category**

Describes the expected behavior for the question.

Common categories include:

- `answerable`: The knowledge base contains sufficient evidence.
- `unanswerable`: The knowledge base does not contain sufficient evidence.
- `ambiguous`: The question needs clarification.
- `multi_hop`: The answer requires combining information from multiple documents.
- `out_of_scope`: The question is outside the application's supported domain.

### Important dataset rules

1. Use questions representative of real users.
2. Include both simple and complex questions.
3. Include questions requiring information from multiple documents.
4. Include unanswerable questions.
5. Record all valid supporting source IDs.
6. Keep reference answers grounded in the source documents.
7. Review the dataset manually to avoid incorrect expected answers.
8. Keep a separate test set that is not used to tune the system.

---

## 14.6 Creating an Evaluation Dataset in Python

Create the following file:

`data/rag_evaluation_dataset.json`

Example contents:

```json
[
  {
    "question": "What does the document say about password recovery?",
    "expected_answer": "The documented recovery procedure.",
    "expected_source_ids": ["doc-001"],
    "category": "answerable"
  },
  {
    "question": "What is the company's office opening time?",
    "expected_answer": "The available documents do not provide this information.",
    "expected_source_ids": [],
    "category": "unanswerable"
  },
  {
    "question": "How do I reset my account password?",
    "expected_answer": "Follow the password reset instructions in the account recovery document.",
    "expected_source_ids": ["doc-001", "doc-004"],
    "category": "answerable"
  },
  {
    "question": "How does the first process affect the second process?",
    "expected_answer": "The answer requires evidence from both relevant documents.",
    "expected_source_ids": ["doc-010", "doc-015"],
    "category": "multi_hop"
  }
]
```

These are illustrative examples. Replace the expected answers and document IDs with information from your own knowledge base.

### Load the dataset

Create `Practical_exercise/load_evaluation_dataset.py`.

```python
import json
from pathlib import Path


DATASET_PATH = Path("data/rag_evaluation_dataset.json")


def load_dataset() -> list[dict]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list):
        raise ValueError("Evaluation dataset must be a list.")

    required_fields = {
        "question",
        "expected_answer",
        "expected_source_ids",
        "category",
    }

    for index, record in enumerate(dataset):
        missing = required_fields - record.keys()

        if missing:
            raise ValueError(
                f"Record {index} is missing fields: {sorted(missing)}"
            )

        if not isinstance(record["expected_source_ids"], list):
            raise ValueError(
                f"Record {index}: expected_source_ids must be a list."
            )

    return dataset


if __name__ == "__main__":
    records = load_dataset()

    print(f"Loaded {len(records)} evaluation questions.")

    for record in records:
        print(f"[{record['category']}] {record['question']}")
```

Run it from the repository root:

```bash
python Practical_exercise/load_evaluation_dataset.py
```

---

## 14.7 Retrieval Recall

### What is Retrieval Recall?

Retrieval Recall measures whether the retriever finds the expected relevant documents or evidence.

It answers:

"Did the retriever find the information needed to answer the question?"

Suppose the expected relevant document IDs are:

```text
doc-001
doc-002
doc-003
```

The retriever returns:

```text
doc-001
doc-003
doc-010
```

Two out of three expected documents were retrieved.

Recall is:

```text
Recall = Relevant Retrieved Documents
         / Total Expected Relevant Documents
```

Therefore:

```text
Recall = 2 / 3 = 0.667
```

Retrieval recall is approximately 66.7%.

### Recall at K

Recall@K measures recall using only the top K retrieved results.

For example, Recall@5 considers the first five retrieved documents.

```text
Recall@K =
Number of expected relevant documents in top K
/
Total number of expected relevant documents
```

### Python implementation

```python
def recall_at_k(
    expected_source_ids: list[str],
    retrieved_source_ids: list[str],
    k: int = 5,
) -> float | None:
    if k < 1:
        raise ValueError("k must be at least 1")

    expected = set(expected_source_ids)

    if not expected:
        return None

    retrieved = set(retrieved_source_ids[:k])

    relevant_retrieved = expected & retrieved

    return len(relevant_retrieved) / len(expected)


expected = ["doc-001", "doc-002", "doc-003"]
retrieved = ["doc-001", "doc-003", "doc-010"]

score = recall_at_k(expected, retrieved, k=3)

print(f"Recall@3: {score:.2%}")
```

Expected output:

```text
Recall@3: 66.67%
```

### When is Recall useful?

Use retrieval recall when:
- Comparing embedding models.
- Comparing chunk sizes.
- Testing top-k values.
- Evaluating hybrid search.
- Checking whether metadata filters remove useful documents.

### Limitations

Document-level recall is only an approximation of evidence retrieval. A retrieved document may not contain the exact passage needed, and one document may be sufficient even when multiple source IDs are listed.

For more precise evaluation, identify relevant passages or chunks and measure evidence recall.

If a question has no expected supporting documents, recall is undefined. Do not automatically assign it a score of zero.

---

## 14.8 Context Precision

### What is Context Precision?

Context Precision measures how much of the retrieved context is relevant to the user's question.

It answers:

"Are the retrieved results useful, or is the system returning too much irrelevant information?"

Suppose the retriever returns five chunks:

```text
Chunk 1: Relevant
Chunk 2: Irrelevant
Chunk 3: Relevant
Chunk 4: Irrelevant
Chunk 5: Relevant
```

A simple precision calculation is:

```text
Precision = Relevant Retrieved Chunks
            / Total Retrieved Chunks
```

Therefore:

```text
Precision = 3 / 5 = 0.60
```

The simple context precision is 60%.

### Precision at K

```text
Precision@K =
Relevant chunks in the top K results
/
K
```

A ranked metric such as Average Precision or a ranking-aware context precision metric gives more credit when relevant evidence appears near the top.

For example, relevant information at rank 1 is generally more useful than relevant information at rank 10.

### Python implementation

```python
def precision_at_k(
    relevant_source_ids: list[str],
    retrieved_source_ids: list[str],
    k: int = 5,
) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")

    retrieved = retrieved_source_ids[:k]

    if not retrieved:
        return 0.0

    relevant = set(relevant_source_ids)

    relevant_count = sum(
        1 for source_id in retrieved
        if source_id in relevant
    )

    return relevant_count / len(retrieved)


expected = ["doc-001", "doc-003"]
retrieved = [
    "doc-001",
    "doc-010",
    "doc-003",
    "doc-020",
    "doc-030",
]

print(f"Precision@5: {precision_at_k(expected, retrieved):.2%}")
```

Expected output:

```text
Precision@5: 40.00%
```

### Important distinction

Source-level precision is not identical to chunk-level context precision.

If a source document contains both relevant and irrelevant passages, counting the entire document as relevant can overestimate quality.

For realistic evaluation, label retrieved chunks or passages as relevant or irrelevant.

### How to improve context precision

- Improve chunk boundaries.
- Use metadata filtering.
- Combine dense and sparse retrieval.
- Apply reranking.
- Remove duplicate chunks.
- Tune the retrieval threshold and top-k setting.

---

## 14.9 Answer Correctness

### What is Answer Correctness?

Answer Correctness measures whether the generated answer matches the reference answer in meaning and factual content.

It answers:

"Did the RAG system answer the question correctly?"

Example:

Expected answer:

```text
Users should follow the documented password recovery procedure.
```

Generated answer:

```text
Use the password recovery instructions provided in the documentation.
```

These answers use different wording but communicate the same idea.

A text comparison based only on identical words would not reliably measure correctness.

### Approaches to answer evaluation

**1. Exact match**

Checks whether the generated answer matches the reference answer exactly after optional normalization.

Useful for:
- Fixed-format answers.
- IDs and short factual outputs.
- Structured fields.

Limitation: correct paraphrases may fail.

**2. Token-level metrics**

Measures word overlap using precision, recall, or F1.

Useful for some extractive tasks, but word overlap alone does not establish factual correctness.

**3. Semantic similarity**

Uses embeddings to compare the meanings of the generated and reference answers.

Limitation: semantically similar answers can still contain different or incorrect facts.

**4. LLM-as-a-judge**

Uses a separate evaluation model to compare the generated answer with the reference answer and supporting evidence.

A judge should evaluate factual correctness, not just fluency.

**5. Human evaluation**

A reviewer checks the answer against the source documents.

Human review is especially useful for high-impact applications, ambiguous questions, and validating automated evaluation methods.

### Simple exact-match implementation

```python
def exact_match(
    generated_answer: str,
    expected_answer: str,
) -> float:
    generated = " ".join(generated_answer.lower().split())
    expected = " ".join(expected_answer.lower().split())

    return float(generated == expected)


print(
    exact_match(
        "Follow the documented procedure.",
        "Follow the documented procedure.",
    )
)
```

Expected output:

```text
1.0
```

This is only a baseline metric. It should not be treated as a complete answer correctness score.

### Answer correctness checklist

- Are the important facts correct?
- Does the answer address the question?
- Does it preserve important conditions and exceptions?
- Does it avoid contradicting the source?
- Does it include the essential information from the reference answer?

---

## 14.10 Faithfulness

### What is Faithfulness?

Faithfulness measures whether the claims in a generated answer are supported by the context provided to the LLM.

It answers:

"Did the model generate an answer using the supplied evidence, or did it introduce unsupported information?"

Example context:

```text
The account recovery procedure requires users to submit a
recovery request through the approved support channel.
```

Generated answer A:

```text
Submit a recovery request through the approved support channel.
```

This answer is supported by the context.

Generated answer B:

```text
Submit a recovery request, and your account will be restored
within exactly five minutes.
```

The five-minute guarantee is unsupported by the context.

Answer B contains an unsupported claim and should receive a lower faithfulness score.

### Claim-based faithfulness evaluation

A practical evaluation process is:

1. Split the answer into factual claims.
2. Identify the evidence supporting each claim.
3. Mark each claim as supported, contradicted, or not supported.
4. Calculate a score using the supported claims.
5. Review contradictions and high-impact unsupported claims separately.

A simple score can be calculated as:

```text
Faithfulness =
Number of supported answer claims
/
Total answer claims
```

This is a simplified metric. Production evaluation should define how contradictions, partial support, and multi-source evidence are handled.

### Example

Generated answer contains four factual claims:

```text
Claim 1: Supported
Claim 2: Supported
Claim 3: Unsupported
Claim 4: Supported
```

Then:

```text
Faithfulness = 3 / 4 = 0.75
```

The simplified faithfulness score is 75%.

### Important distinction: correctness versus faithfulness

An answer may be factually correct according to outside knowledge but unfaithful to the retrieved context.

For example, the model may provide a generally valid password security recommendation that the documents never mention.

In a strict RAG application, the answer may still violate the requirement to use only approved evidence.

Likewise, an answer can faithfully repeat an incorrect statement in a source document. Faithfulness does not independently establish that the source itself is true.

### How to improve faithfulness

- Use clear prompts that require evidence-based answers.
- Include relevant passages in the context.
- Avoid excessively large or noisy contexts.
- Ask the model to acknowledge missing information.
- Verify important claims against the retrieved sources.
- Evaluate unsupported claims separately from stylistic quality.

---

## 14.11 Citation Accuracy

### What is Citation Accuracy?

Citation Accuracy measures whether the sources cited in an answer actually support the claims associated with them.

It answers:

"Does the citation prove what the answer says?"

Example:

Generated answer:

```text
Users must submit a recovery request through the support channel.
[doc-001]
```

If `doc-001` contains this procedure, the citation is appropriate.

If `doc-001` discusses account registration instead, the citation does not support the claim.

### Citation evaluation dimensions

**Citation precision**

Of the citations provided, how many correctly support their associated claims?

**Citation coverage**

Of the claims that require evidence, how many have at least one supporting citation?

**Source correctness**

Does the citation point to the correct source, document, or passage?

**Citation completeness**

Are important factual claims supported by citations where the application requires them?

### Simple citation precision

```text
Citation Precision =
Number of valid citations
/
Total citations
```

### Simple citation coverage

```text
Citation Coverage =
Number of factual claims with supporting citations
/
Total factual claims requiring citations
```

Example:

An answer contains four factual claims. Three have valid supporting citations.

```text
Citation Coverage = 3 / 4 = 75%
```

If the answer has no citations, citation precision is undefined rather than automatically perfect. Citation coverage is zero when factual claims require citations.

### Python implementation

```python
def citation_precision(
    citation_validity: list[bool],
) -> float | None:
    if not citation_validity:
        return None

    valid_count = sum(citation_validity)

    return valid_count / len(citation_validity)


def citation_coverage(
    claims_requiring_citations: int,
    claims_with_supporting_citations: int,
) -> float | None:
    if claims_requiring_citations < 0:
        raise ValueError("Claim count cannot be negative")

    if claims_with_supporting_citations < 0:
        raise ValueError("Supported claim count cannot be negative")

    if claims_with_supporting_citations > claims_requiring_citations:
        raise ValueError("Supported claim count cannot exceed total")

    if claims_requiring_citations == 0:
        return None

    return (
        claims_with_supporting_citations
        / claims_requiring_citations
    )


print(citation_precision([True, True, False, True]))
print(citation_coverage(4, 3))
```

Expected output:

```text
0.75
0.75
```

These functions assume citation validity has already been checked against the source evidence.

### Common citation errors

- Citing a document that does not support the claim.
- Using a nonexistent source ID.
- Citing the right document but the wrong passage.
- Providing citations that do not cover the main answer.
- Attaching a valid citation to an unrelated sentence.
- Generating a source URL that does not correspond to a retrieved source.

### Best practices

- Keep source IDs and URLs in retrieval metadata.
- Associate citations with specific answer claims.
- Check citations against the actual retrieved evidence.
- Never invent document IDs or URLs.
- Test citation behavior independently from answer correctness.

---

## 14.12 Latency Evaluation

### What is Latency?

Latency measures how long the RAG system takes to process a question and return an answer.

A RAG request may include several time-consuming stages:

```text
Request Received
      |
      v
Query Processing
      |
      v
Retrieval
      |
      v
Reranking
      |
      v
Prompt Construction
      |
      v
LLM Generation
      |
      v
Citation Formatting
      |
      v
Response Completed
```

### Useful latency metrics

**Retrieval latency**

Time taken to search the knowledge base and retrieve relevant context.

**Reranking latency**

Time taken to reorder candidate documents, when reranking is enabled.

**Time to first token (TTFT)**

Time from request initiation until the first generated token becomes available.

**Generation latency**

Time spent generating the response.

**End-to-end latency**

Time from the beginning of the request until the final answer is completed.

**P50, P95, and P99 latency**

- P50: the median response time.
- P95: the time within which 95% of requests finish.
- P99: the time within which 99% of requests finish.

Percentiles are more informative than averages alone when evaluating a production system.

### Python implementation

```python
import time


def evaluate_retrieval(retrieve, question: str):
    start = time.perf_counter()

    documents = retrieve(question)

    elapsed_ms = (time.perf_counter() - start) * 1000

    return documents, elapsed_ms
```

Usage:

```python
def mock_retrieve(question: str) -> list[str]:
    return ["doc-001", "doc-002"]


documents, latency_ms = evaluate_retrieval(
    mock_retrieve,
    "What is RAG?",
)

print("Documents:", documents)
print(f"Retrieval latency: {latency_ms:.2f} ms")
```

This example measures retrieval only. The actual time depends on the implementation and environment.

### Measuring end-to-end latency

```python
def evaluate_rag_request(retrieve, generate, question: str):
    start = time.perf_counter()

    documents = retrieve(question)
    retrieval_finished = time.perf_counter()

    answer = generate(question, documents)
    generation_finished = time.perf_counter()

    return {
        "answer": answer,
        "retrieved_documents": documents,
        "retrieval_latency_ms": (
            retrieval_finished - start
        ) * 1000,
        "generation_latency_ms": (
            generation_finished - retrieval_finished
        ) * 1000,
        "total_latency_ms": (
            generation_finished - start
        ) * 1000,
    }
```

The `retrieve` and `generate` functions are placeholders for your actual RAG components.

### Performance testing rules

- Run multiple requests rather than relying on one measurement.
- Separate cold-start latency from steady-state latency.
- Measure under realistic concurrency.
- Track timeouts and failed requests.
- Record model, prompt, retrieval settings, and hardware.
- Compare latency alongside quality metrics.
- Measure streaming TTFT separately when streaming is supported.

---

## 14.13 Failure Handling and Unanswerable Questions

### What is Failure Handling Evaluation?

Failure handling evaluation checks whether the system behaves correctly when it cannot produce a reliable answer.

A good RAG system should not answer every question at any cost.

It should recognize when:
- No relevant documents were retrieved.
- Retrieved context does not contain sufficient evidence.
- The question is ambiguous.
- The question is outside the supported domain.
- Retrieval or generation fails.
- A required source is unavailable.

### Example

User question:

```text
What is the office opening time?
```

Suppose the knowledge base contains no information about office opening times.

An inappropriate answer would invent an opening time.

An appropriate answer would explain that the available documents do not provide this information and, where appropriate, direct the user to an approved support channel.

### Evaluation categories

**Answerable**

Sufficient evidence exists, so the system should answer correctly.

**Unanswerable**

Sufficient evidence is missing, so the system should abstain or use the configured fallback.

**Ambiguous**

The question has multiple plausible interpretations, so the system may need clarification.

**Out of scope**

The question is outside the application's supported domain, so the system should use the appropriate scope response.

**Retrieval or generation error**

A component fails, so the system should return a safe, controlled failure response instead of fabricated content.

### Useful failure-handling metrics

**Abstention rate on unanswerable questions**

The proportion of unanswerable questions for which the system abstains appropriately.

**Answer rate on answerable questions**

The proportion of answerable questions for which the system attempts to provide an answer.

**False answer rate**

The proportion of unanswerable questions for which the system provides an unsupported substantive answer.

**Appropriate fallback rate**

The proportion of cases requiring fallback in which the correct fallback behavior occurs.

### Python implementation

```python
def evaluate_failure_handling(
    category: str,
    generated_answer: str,
    abstained: bool,
) -> dict:
    if category == "unanswerable":
        return {
            "expected_behavior": "abstain",
            "passed": abstained,
        }

    if category == "answerable":
        return {
            "expected_behavior": "answer",
            "passed": (
                not abstained
                and bool(generated_answer.strip())
            ),
        }

    if category == "ambiguous":
        return {
            "expected_behavior": "clarify_or_safe_fallback",
            "passed": abstained,
        }

    if category == "out_of_scope":
        return {
            "expected_behavior": "scope_fallback",
            "passed": abstained,
        }

    return {
        "expected_behavior": "manual_review",
        "passed": None,
    }
```

This is a simple illustrative checker. In a real application, asking a clarifying question may be valid even when `abstained` is false. Failure evaluation should inspect the actual response behavior, not only a single boolean.

### Important consideration

A low answer rate is not necessarily good. A system that abstains on every question avoids many hallucinations but is not useful.

Evaluate answerability, correctness, and appropriate abstention together.

---

### Important limitations of this exercise

The mock functions are used to demonstrate the evaluation workflow. They do not call a real embedding model, vector database, or LLM.

The example measures retrieval recall, exact match, and latency only.

It does not automatically evaluate:
- Context precision.
- Faithfulness.
- Citation support.
- Semantic answer correctness.
- Appropriate failure handling.

Replace the mock functions with your real RAG pipeline before interpreting the scores as system performance.

Also ensure that your dataset's expected answers match the documents used by the actual retriever.

---

## 14.15 Aggregating Evaluation Results

Evaluating individual questions is useful, but aggregate metrics help compare system versions.

For example, you may evaluate 100 questions and calculate average retrieval recall and answer correctness.

### Mean metric score

```text
Mean Score =
Sum of valid individual scores
/
Number of valid individual scores
```

Do not include undefined values as zero. Report the number of valid observations for each metric.

### Python implementation

```python
def mean_score(scores: list[float | None]) -> float | None:
    valid_scores = [
        score for score in scores
        if score is not None
    ]

    if not valid_scores:
        return None

    return sum(valid_scores) / len(valid_scores)


scores = [0.8, 0.6, None, 1.0]

print(mean_score(scores))
```

Expected output:

```text
0.8
```

### Recommended aggregate report

| Metric | Example result |
|---|---:|
| Recall@5 | 0.90 |
| Context Precision | 0.82 |
| Answer Correctness | 0.88 |
| Faithfulness | 0.95 |
| Citation Precision | 0.97 |
| Citation Coverage | 0.91 |
| P50 Latency | 1.2 seconds |
| P95 Latency | 3.8 seconds |
| Unanswerable False Answer Rate | 0.04 |

These numbers are illustrative only, not actual benchmark results.

### Report metrics by category

Calculate metrics separately for:
- Answerable questions.
- Unanswerable questions.
- Ambiguous questions.
- Multi-hop questions.
- Out-of-scope questions.

An overall average can hide failures in a specific category.

---

## 14.16 Using LLM-as-a-Judge

LLM-as-a-judge uses a language model to assess the quality of another model's response.

It is useful for evaluating dimensions that cannot be reliably measured through exact string comparison.

Examples include:
- Answer correctness.
- Faithfulness.
- Context relevance.
- Citation support.

### Example judge prompt

```text
You are evaluating a Retrieval-Augmented Generation system.

Evaluate the answer using only the supplied context and reference answer.

Question:
{question}

Reference answer:
{expected_answer}

Retrieved context:
{retrieved_context}

Generated answer:
{generated_answer}

Return a JSON object with these fields:

{
  "answer_correctness": 0,
  "faithfulness": 0,
  "context_relevance": 0,
  "unsupported_claims": [],
  "explanation": ""
}

Scoring:
0 = Incorrect or unsupported
1 = Partially correct or partially supported
2 = Fully correct or fully supported

Rules:
- Do not reward fluent writing if the facts are wrong.
- Do not assume facts that are absent from the context.
- Identify unsupported factual claims.
- Distinguish a missing answer from an incorrect answer.
- Do not invent evidence or citations.
- Follow the supplied scoring definitions consistently.
```

This prompt illustrates the evaluation design. It is not a complete evaluator implementation.

### Limitations of LLM-as-a-judge

- The judge may make mistakes.
- The judge may prefer longer or more fluent answers.
- Different judge models may produce different scores.
- The judge may miss subtle factual errors.
- A model can agree with an answer that is unsupported by the evidence.

### Best practices

1. Use a consistent evaluation prompt.
2. Use a fixed judge model and record its version.
3. Validate a sample of results with human reviewers.
4. Keep reference answers and supporting documents available.
5. Do not treat judge scores as unquestionable ground truth.
6. Use deterministic or structured outputs where supported.

---

## 14.17 RAG Evaluation Frameworks

Several frameworks can help automate evaluation.

### Ragas

Ragas provides metrics and workflows for evaluating RAG applications. Depending on the configured metric, evaluation may require questions, retrieved contexts, generated answers, reference answers, or reference evidence.

Commonly discussed metric families include faithfulness, answer relevance, context precision, context recall, and answer correctness.

Official documentation:

https://docs.ragas.io/

### DeepEval

DeepEval provides evaluation tests for LLM applications, including RAG-related metrics and LLM-as-a-judge workflows.

Official documentation:

https://docs.confident-ai.com/

### Custom evaluation

A custom evaluation pipeline is useful when:
- The application has specific business rules.
- Citation behavior must follow a particular format.
- Unanswerable questions require strict fallback behavior.
- Retrieval source IDs have application-specific meanings.
- Latency must be measured at individual pipeline stages.

### Choosing an approach

Start with a small, transparent custom evaluation script. Once the dataset and expected behavior are well defined, add a framework if it reduces implementation effort.

Frameworks do not eliminate the need for a reliable evaluation dataset and manual validation.

---

## 14.18 Regression Testing for RAG

Regression testing checks whether a change improves or damages previously working behavior.

Changes that can affect RAG quality include:
- Embedding model changes.
- Chunk-size changes.
- Chunk-overlap changes.
- Retrieval top-k changes.
- BM25 or hybrid search changes.
- Reranker changes.
- Prompt changes.
- LLM model changes.
- Citation formatting changes.
- Metadata filters.

### Example workflow

```text
Version A: Current RAG System
          |
          v
Run Fixed Evaluation Dataset
          |
          v
Record Baseline Metrics
          |
          v
Change Retrieval or Generation
          |
          v
Run the Same Dataset
          |
          v
Compare Metrics
          |
          v
Accept or Reject the Change
```

### Regression checklist

- Did retrieval recall improve?
- Did context precision decrease?
- Did answer correctness improve?
- Did faithfulness decrease?
- Are citations still accurate?
- Did P95 latency increase?
- Are unanswerable questions handled correctly?
- Did any previously correct question become incorrect?

Do not optimize only one metric. A reranker that improves precision but removes necessary evidence may reduce recall and answer quality.

---

## 14.19 Common RAG Evaluation Mistakes

### Mistake 1: Evaluating only the final answer

A wrong answer may result from bad retrieval or bad generation.

**Solution:** Measure retrieval and generation separately.

### Mistake 2: Using only exact match

Correct paraphrases may receive zero.

**Solution:** Combine exact match with semantic or rubric-based factual evaluation.

### Mistake 3: Ignoring unanswerable questions

The system may appear accurate because every test question has an answer in the dataset.

**Solution:** Include questions for which evidence is absent.

### Mistake 4: Confusing faithfulness with correctness

A response may repeat retrieved text faithfully but still fail to answer the user's question correctly.

**Solution:** Evaluate faithfulness and answer correctness separately.

### Mistake 5: Counting citations without verifying support

An answer can contain many citations that do not prove its claims.

**Solution:** Check each citation against its associated claim and source passage.

### Mistake 6: Evaluating on too few questions

A small test set may not represent real usage.

**Solution:** Use a diverse dataset and increase it as the application evolves.

### Mistake 7: Using test questions to tune the system repeatedly

Repeatedly optimizing against the same small test set can cause overfitting.

**Solution:** Keep separate development, validation, and held-out test sets.

### Mistake 8: Ignoring latency and reliability

A high-quality answer is less useful if most requests time out.

**Solution:** Measure latency percentiles, timeouts, and failure rates under realistic workloads.

### Mistake 9: Trusting automated judges without validation

An evaluator can make the same types of mistakes as the generator.

**Solution:** Manually inspect a representative sample of scored answers.

---

## 14.20 Production RAG Evaluation Strategy

A production-ready evaluation process should contain the following stages.

### Stage 1: Build a representative dataset

Include real user questions, expected answers, supporting source IDs, and unanswerable examples.

Remove sensitive information and ensure that the dataset is approved for evaluation.

### Stage 2: Establish a baseline

Run the existing RAG pipeline and record:
- Retrieval metrics.
- Answer quality metrics.
- Citation metrics.
- Latency percentiles.
- Failure-handling metrics.

### Stage 3: Identify the source of failure

For every failed question, inspect:
- The original question.
- The retrieved documents and chunks.
- Retrieval rankings and scores.
- The prompt sent to the LLM.
- The generated answer.
- The citations.
- The component timings.

### Stage 4: Make a targeted improvement

Change one major variable at a time when possible. Examples include chunking, retrieval settings, reranking, or prompting.

### Stage 5: Run regression tests

Evaluate the modified system against the same test set and compare metrics.

### Stage 6: Perform human review

Inspect incorrect answers, unsupported claims, citation failures, and borderline cases.

### Stage 7: Monitor production behavior

Track quality indicators and system performance over time. Use privacy-aware logging and follow the application's data retention rules.

### Stage 8: Expand the dataset

Add representative failure cases discovered during development and production monitoring.

Do not add unverified expected answers. Each new test case should be reviewed against trusted source material.

---

## 14.21 Practical Exercises

Complete these exercises in order.

### Exercise 1: Create the dataset

Create `data/rag_evaluation_dataset.json` with at least 20 questions.

Include:
- 10 answerable questions.
- 5 unanswerable questions.
- 3 multi-hop questions.
- 2 ambiguous or out-of-scope questions.

Verify the expected answers against your knowledge base.

### Exercise 2: Measure retrieval recall

For each answerable question:
1. Retrieve the top five chunks.
2. Record the retrieved source IDs.
3. Compare them with expected source IDs.
4. Calculate Recall@5.
5. Find the questions with low recall.

### Exercise 3: Measure context precision

Label each retrieved chunk as relevant or irrelevant.

Calculate Precision@5 and inspect cases where irrelevant chunks dominate the context.

### Exercise 4: Evaluate answer correctness

Compare generated answers with the expected answers.

Start with exact match, then manually assess paraphrases and factual correctness.

### Exercise 5: Evaluate faithfulness

Identify factual claims in generated answers.

For each claim, locate supporting evidence or mark the claim as unsupported.

### Exercise 6: Verify citations

Check that every required citation points to a real source and supports its associated claim.

Calculate citation precision and coverage.

### Exercise 7: Measure latency

Record retrieval, generation, and end-to-end latency for each question.

Calculate P50 and P95 latency from repeated measurements.

### Exercise 8: Test unanswerable questions

Verify that the system does not invent answers when evidence is missing.

Calculate the false answer rate.

### Exercise 9: Compare retrieval configurations

Compare:
- Dense retrieval.
- Keyword retrieval.
- Hybrid retrieval.
- Hybrid retrieval with reranking.

Use the same evaluation dataset for every configuration.

### Exercise 10: Write an evaluation report

Summarize the metrics, important failures, proposed fixes, and the results of regression testing.

---

## 14.22 Suggested Evaluation Results Table

Use a table like this when recording experiment results.

| Experiment | Recall@5 | Precision@5 | Correctness | Faithfulness | Citation Precision | P95 Latency |
|---|---:|---:|---:|---:|---:|---:|
| Dense retrieval | — | — | — | — | — | — |
| Keyword retrieval | — | — | — | — | — | — |
| Hybrid retrieval | — | — | — | — | — | — |
| Hybrid + reranking | — | — | — | — | — | — |

Fill in the values obtained from actual evaluation runs.

Use the same test set, evaluation rules, and relevant generation settings when comparing experiments. Report sample sizes and undefined metrics rather than silently treating missing values as zero.

---

## 14.23 Architecture Diagram: RAG Evaluation Pipeline

```text
                  Evaluation Dataset
                          |
                          v
                    User Question
                          |
                          v
                    RAG Pipeline
                          |
             +------------+------------+
             |                         |
             v                         v
      Retrieved Context          Generated Answer
             |                         |
             v                         v
      Retrieval Evaluation      Answer Evaluation
             |                         |
             v                         v
       Recall / Precision       Correctness / Faithfulness
                                       |
                                       v
                               Citation Evaluation
                                       |
                                       v
                                 Latency Metrics
                                       |
                                       v
                             Failure-Handling Tests
                                       |
                                       v
                              Evaluation Report
                                       |
                                       v
                           Regression Comparison
```

---

## 14.24 Key Takeaways

1. RAG evaluation measures retrieval, generation, and end-to-end system quality.
2. Retrieval Recall measures whether expected evidence was found.
3. Context Precision measures the relevance of retrieved context.
4. Answer Correctness measures whether the generated answer is factually correct.
5. Faithfulness measures whether the answer is supported by the supplied context.
6. Citation Accuracy measures whether citations actually support the claims.
7. Latency measures system speed and responsiveness.
8. Failure Handling checks whether the system abstains or uses the appropriate fallback when evidence is insufficient.
9. A fixed evaluation dataset makes comparisons and regression testing more reliable.
10. Automated metrics and LLM judges should be validated with human review.
11. Production evaluation must balance answer quality, evidence quality, reliability, and speed.
12. No single metric fully describes RAG quality.

---

## 14.25 Lesson 14 Completion Checklist

- [ ] Understand the major dimensions of RAG evaluation.
- [ ] Create an evaluation dataset with expected answers and source IDs.
- [ ] Implement Recall@K.
- [ ] Implement Precision@K.
- [ ] Understand answer correctness and its limitations.
- [ ] Understand faithfulness and unsupported claims.
- [ ] Implement citation precision and citation coverage checks.
- [ ] Measure retrieval and end-to-end latency.
- [ ] Test unanswerable questions and fallback behavior.
- [ ] Save evaluation results as JSON or CSV.
- [ ] Compare multiple retrieval configurations.
- [ ] Write a regression evaluation report.
- [ ] Commit the notes and exercises to GitHub.


