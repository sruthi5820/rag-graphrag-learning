# Lesson 19: Production RAG and GraphRAG Architecture

File: `notes/19-production-architecture.md`

## 19.1 Definition

Production RAG and GraphRAG architecture describes how to design, deploy, secure, monitor, and maintain a retrieval-augmented generation application for real users.

A learning project may run as one Python script. A production application needs additional components to handle:

- Multiple concurrent users.
- Large document collections.
- Authentication and authorization.
- Reliable retrieval and answer generation.
- Data updates and index versioning.
- Failures, timeouts, and retries.
- Monitoring, evaluation, and deployment.

The most important architectural principle is to **separate the offline indexing pipeline from the online question-answering pipeline**.

### 1. Offline indexing pipeline

The offline pipeline prepares information before users ask questions.

Typical steps:

1. Collect documents from approved sources.
2. Parse documents and extract text.
3. Clean and normalize the content.
4. Split content into chunks.
5. Generate embeddings.
6. Extract entities and relationships when using GraphRAG.
7. Build or update the vector index and knowledge graph.
8. Generate community summaries if required.
9. Validate the new index.
10. Publish a version that the online application can use.

The pipeline runs when documents are added, changed, deleted, or reprocessed.

### 2. Online question-answering pipeline

The online pipeline processes user questions.

Typical steps:

1. Receive the request through an API.
2. Authenticate the user.
3. Validate the request.
4. Check the user's permissions.
5. Retrieve relevant documents, graph evidence, or summaries.
6. Rank and filter the retrieved evidence.
7. Construct a prompt using approved evidence.
8. Generate an answer with an LLM.
9. Validate the answer and citations.
10. Return the response.
11. Record relevant performance and quality metrics.

This pipeline runs whenever a user asks a question.

### Example

Imagine a company has 50,000 internal documents.

The offline pipeline processes the documents and creates the necessary indexes.

When an employee asks:

"What is our password reset procedure?"

the online pipeline retrieves the relevant passages, checks that the employee can access them, and asks the LLM to answer using the retrieved evidence.

The application should not reprocess all 50,000 documents for every question.

---

## 19.2 Why It Matters

A prototype may work for one user and a few documents but fail when deployed to many users.

Production architecture helps make a RAG application reliable, secure, scalable, and maintainable.

### 1. Performance

Users expect answers within a reasonable amount of time.

Separate indexing from query processing so document parsing, embedding generation, and graph construction do not unnecessarily delay normal questions.

### 2. Scalability

A production application may receive many requests at the same time.

The API, retrieval system, and model-serving infrastructure should be designed to handle the expected workload.

### 3. Security

Documents may contain private or restricted information.

The application must check permissions before retrieving evidence and before returning information to the user.

### 4. Reliability

External model services, databases, vector stores, and network connections can fail.

Timeouts, controlled retries, fallback behavior, and error handling prevent many failures from becoming application-wide outages.

### 5. Maintainability

Documents change over time. A production system needs a safe process to update indexes without accidentally making incomplete or inconsistent data available.

### 6. Quality

A fast answer is not necessarily a correct answer.

Production systems should evaluate retrieval relevance, answer correctness, citation accuracy, and whether claims are supported by evidence.

### 7. Observability

Logs, metrics, and traces help engineers understand why a request was slow, why retrieval failed, or why an answer was incorrect.

**Main idea:** Production RAG is not just an LLM connected to a vector database. It is a complete application with data pipelines, retrieval, security, infrastructure, evaluation, and operations.

---

## 19.3 Key Concepts

### 1. Offline and Online Workloads

Offline and online workloads have different requirements.

| Area | Offline indexing | Online question answering |
|---|---|---|
| Main purpose | Prepare searchable information | Answer user questions |
| Typical trigger | New or changed documents | User request |
| Main work | Parsing, chunking, embeddings, graph construction | Retrieval, ranking, generation |
| Latency requirement | Usually minutes or longer, depending on the workload | Usually seconds or another defined response target |
| Failure handling | Retry, quarantine, or reject failed documents | Return a controlled error or safe fallback |
| Scaling | Batch workers and queues | API workers, retrieval services, model servers |
| Main measurements | Processing throughput and indexing failures | Latency, throughput, answer quality |

The two pipelines can share storage and services, but they should not be tightly coupled.

### 2. API Design and Request Validation

An API allows a frontend or another application to communicate with the RAG backend.

A typical request might contain:

```json
{
  "question": "What is retrieval-augmented generation?",
  "top_k": 5
}
```

The API should validate:

- Whether the question is present.
- Whether the question contains valid text.
- Whether the request exceeds the maximum allowed length.
- Whether `top_k` is within an allowed range.
- Whether the user is authenticated.
- Whether the user has permission to access the requested information.

Use structured request and response models rather than accepting arbitrary input.

### 3. Authentication and Authorization

These concepts are related but different.

**Authentication:** Determines who the user is.

**Authorization:** Determines what the user is allowed to access.

For example, an employee may successfully log in but still be prohibited from retrieving HR documents.

A production RAG system should enforce access control at retrieval time.

Do not rely on the LLM to decide whether a user is allowed to see a document.

### 4. Document-Level Access Control

Each document or chunk may have access-control metadata.

Example:

```python
{
    "document_id": "doc-100",
    "department": "engineering",
    "allowed_groups": [
        "engineering",
        "administrators"
    ]
}
```

The retrieval system must filter results according to the authenticated user's permissions.

Important considerations:

- Apply permission filters before evidence is passed to the LLM.
- Apply them to vector and graph retrieval.
- Ensure community summaries do not reveal restricted information.
- Prevent caches from returning one user's private results to another user.
- Recheck permissions when document access changes.

For graph-based systems, a public entity can have relationships to private entities. Access to one entity does not automatically authorize access to every connected node.

### 5. Index Versioning

An index version identifies a particular processed version of the document collection.

For example:

```text
index-v1
index-v2
index-v3
```

Suppose `index-v1` is serving production traffic while `index-v2` is being built.

The application should continue using `index-v1` until `index-v2` has been validated and is ready to serve.

After validation, the active index can be switched to `index-v2`.

This approach is safer than modifying the live index without a recovery plan.

### 6. Incremental Indexing

Incremental indexing processes only the documents that have changed instead of rebuilding everything unnecessarily.

The pipeline should identify:

- New documents.
- Modified documents.
- Deleted documents.
- Documents that failed processing.
- Documents whose embedding model or processing configuration changed.

A document change may require updating its chunks, embeddings, graph relationships, and community summaries.

For example, deleting a source document should also remove or invalidate its indexed chunks and any derived evidence that is no longer supported.

### 7. Caching

Caching stores the results of expensive operations so they can be reused.

Possible cache targets include:

- Query embeddings.
- Retrieval results.
- Community summaries.
- Final answers, when safe.
- Metadata lookups.

A cache key must account for relevant inputs.

For a final-answer cache, these may include:

- Normalized question.
- User or permission scope.
- Active index version.
- Retrieval configuration.
- Model and prompt version, when relevant.

Never use only the question as the cache key if different users can access different documents.

A cache must not bypass authorization or return stale information after a relevant document changes.

### 8. Rate Limiting

Rate limiting controls how many requests a user or client can send within a time window.

For example:

```text
Maximum: 30 requests per minute per user
```

This is an illustrative limit, not a universal recommendation.

Rate limiting helps prevent accidental overload, automated abuse, and excessive model usage.

In a multi-worker deployment, use a shared rate-limiting mechanism when a consistent limit across all workers is required.

### 9. Timeouts and Retries

A timeout limits how long an operation can wait.

For example:

```python
timeout_seconds = 30
```

A retry attempts an operation again after a failure.

Retries are useful for transient errors, but they should be limited and controlled.

Good retry behavior includes:

- A maximum number of attempts.
- Exponential backoff.
- Random jitter to avoid synchronized retries.
- Retrying only errors that may be temporary.
- Avoiding duplicate side effects.
- Respecting the overall request deadline.

Do not automatically retry every failure. Invalid input, authorization failures, and permanent configuration errors usually require different handling.

### 10. Circuit Breakers

A circuit breaker temporarily stops calls to a service that is repeatedly failing.

For example, if an LLM endpoint becomes unavailable, the application may stop sending requests to it for a short period rather than repeatedly waiting for timeouts.

Typical states are:

- **Closed:** Calls are allowed.
- **Open:** Calls are blocked temporarily.
- **Half-open:** A limited number of test calls determine whether the service has recovered.

Circuit breakers are especially useful when one failing dependency could otherwise exhaust application workers.

### 11. Structured Logging

Structured logs store events in a consistent format, such as JSON.

Example:

```json
{
  "event": "retrieval_completed",
  "request_id": "req-123",
  "retrieved_chunks": 5,
  "duration_ms": 120
}
```

Useful fields include:

- Request ID.
- Trace ID.
- Operation name.
- Duration.
- Retrieval count.
- Index version.
- Error category.
- Model name.

Avoid logging passwords, access tokens, private document contents, or unnecessary personal information.

### 12. Distributed Tracing

Distributed tracing follows a request across multiple services.

A single RAG request may pass through:

1. API gateway.
2. Authentication.
3. Query embedding.
4. Vector retrieval.
5. Graph retrieval.
6. Reranking.
7. LLM generation.
8. Citation validation.

A trace helps identify which operation caused a delay.

For example, if the total response time is 4 seconds and LLM generation takes 3 seconds, optimizing the graph query alone may have little effect on the overall latency.

### 13. Metrics

Metrics are numerical measurements used to understand system behavior.

Useful production metrics include:

- Requests per second.
- Error rate.
- Retrieval latency.
- LLM latency.
- End-to-end latency.
- Token usage.
- Cache hit rate.
- Queue depth.
- Indexing throughput.
- Retrieval relevance.
- Answer correctness.
- Citation correctness.

Measure quality and system performance separately.

A system can have low latency but poor answers, or excellent answers but unacceptable latency.

### 14. Concurrency and Backpressure

Concurrency is the number of operations that can run at the same time.

Backpressure prevents the application from accepting more work than it can safely process.

For example, if the LLM server supports only a limited number of simultaneous requests, the API may use a bounded queue or semaphore to limit active generation requests.

Without limits, incoming requests can consume memory, occupy workers, and cause cascading failures.

### 15. Deployment and Rollback

A deployment procedure should support:

- Configuration validation.
- Dependency and security checks.
- Automated tests.
- Index compatibility checks.
- Health checks.
- Controlled traffic switching.
- Monitoring after deployment.
- Rollback if the new release fails.

The application version and index version should be tracked separately because they can change independently.

### 16. GraphRAG-Specific Production Concerns

GraphRAG adds components beyond ordinary vector-based RAG.

These may include:

- Entity extraction.
- Entity resolution.
- Relationship extraction.
- Graph storage.
- Graph traversal.
- Community detection.
- Community report generation.
- Graph and summary versioning.

A graph update can affect several derived artifacts.

For example, changing an entity or relationship may require updating affected community summaries and graph indexes.

The system should maintain provenance so generated summaries can be traced to their source documents.

Use graph retrieval where it improves the evidence available for a question. Simple factual questions may still be served efficiently by vector retrieval alone.

---

## 19.4 Architecture

A production system should separate offline indexing and online question answering.

### Architecture diagram

```mermaid
flowchart TB
    subgraph OFFLINE["Offline Indexing Pipeline"]
        A[Source Documents] --> B[Parsing and Cleaning]
        B --> C[Chunking]
        C --> D[Generate Embeddings]
        C --> E[Entity and Relationship Extraction]
        E --> F[Build Knowledge Graph]
        D --> G[Build Vector Index]
        F --> H[Community Detection and Summaries]
        G --> I[Validate Index]
        H --> I
        I --> J[Publish Index Version]
    end

    subgraph ONLINE["Online Question-Answering Pipeline"]
        K[User] --> L[API Gateway]
        L --> M[Authentication and Authorization]
        M --> N[Request Validation]
        N --> O[Query Processing]
        O --> P[Vector Retrieval]
        O --> Q[Graph Retrieval]
        P --> R[Merge and Rerank Evidence]
        Q --> R
        R --> S[Access and Evidence Validation]
        S --> T[LLM Generation]
        T --> U[Citation Validation]
        U --> V[Answer]
    end

    J --> G
    J --> F
    J --> H

    L --> W[Rate Limiting]
    W --> M

    L --> X[Logs, Metrics and Traces]
    O --> X
    R --> X
    T --> X
```

### Explanation

**Offline pipeline**

- Prepares source data.
- Creates chunks and embeddings.
- Extracts entities and relationships when needed.
- Builds the vector index and graph.
- Detects communities and generates summaries if the application needs them.
- Validates and publishes an index version.

**Online pipeline**

- Accepts and validates requests.
- Authenticates the user and enforces access control.
- Retrieves evidence from the relevant indexes.
- Combines and ranks evidence.
- Generates an answer using the selected evidence.
- Checks citations and returns the result.

**Shared operational services**

Rate limiting, logs, metrics, traces, configuration, and deployment controls support both pipelines.

The diagram is a logical architecture. In a small deployment, several components may run in one service. At larger scale, components may be deployed independently.

---

## 19.5 Python Implementation

### Goal

Build a small FastAPI service that demonstrates production-oriented API practices.

This exercise demonstrates:

1. Structured request validation.
2. Authentication using a configured API token.
3. A bounded retrieval result count.
4. A request identifier.
5. A timeout for a simulated retrieval operation.
6. A controlled error response.
7. Basic structured logging.
8. A health endpoint.

The retrieval function is a mock. It does not connect to a real vector database, knowledge graph, or LLM. This keeps the exercise runnable while demonstrating the service structure.

Do not treat this example as a complete production authentication system. In a real deployment, use an appropriate identity provider or validated user-token system, enforce document-level permissions, and store secrets securely.

### Step 1: Install dependencies

Activate your project's virtual environment:

```bash
source .venv/bin/activate
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

### Step 2: Create the Python file

Create:

`Practical_exercise/production_rag_api_19.py`

Copy this code:

```python
"""
Lesson 19: Production RAG API Basics

This example demonstrates:
- Request validation.
- API token authentication.
- Request IDs.
- Retrieval timeouts.
- Controlled error handling.
- Structured logging.
- A health endpoint.

The retrieval function is a mock.
It does not call a real vector database or LLM.
"""

import asyncio
import hmac
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field


# ============================================================
# 1. CONFIGURATION
# ============================================================

# Read the token from an environment variable.
# Never hardcode a real production secret in source code.

API_TOKEN = os.getenv("RAG_API_TOKEN")

# This is an example timeout.
# Production values should be based on measured latency
# and the application's end-to-end request deadline.

RETRIEVAL_TIMEOUT_SECONDS = 2.0


# ============================================================
# 2. LOGGING
# ============================================================

# Use structured key-value fields in log messages so that
# monitoring systems can search and filter events.

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(levelname)s "
        "%(name)s %(message)s"
    ),
)

logger = logging.getLogger("production_rag")


# ============================================================
# 3. REQUEST AND RESPONSE MODELS
# ============================================================

class AskRequest(BaseModel):
    """
    Defines the accepted JSON request.

    Pydantic validates the input before the endpoint runs.
    """

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Question to answer using retrieved evidence",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of evidence passages",
    )


class AskResponse(BaseModel):
    """
    Defines the JSON response returned by the API.
    """

    request_id: str
    answer: str
    citations: list[str]
    retrieval_count: int
    duration_ms: int


# ============================================================
# 4. AUTHENTICATION
# ============================================================

async def require_api_token(
    authorization: str | None = Header(default=None),
) -> None:
    """
    Validate a simple bearer token for this learning exercise.

    A real application should validate user identity and
    permissions through its configured authentication system.

    The API fails closed if the token is not configured.
    """

    if not API_TOKEN:
        logger.error("Authentication token is not configured")

        raise HTTPException(
            status_code=503,
            detail="Authentication is not configured",
        )

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, separator, supplied_token = (
        authorization.partition(" ")
    )

    if (
        not separator
        or scheme.lower() != "bearer"
        or not supplied_token
        or not hmac.compare_digest(
            supplied_token,
            API_TOKEN,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============================================================
# 5. APPLICATION LIFECYCLE
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Validate required configuration when the service starts.

    A real application may also initialize database clients,
    vector-store connections, model clients, and other resources
    here. Those clients should be closed during shutdown.
    """

    if not API_TOKEN:
        logger.warning(
            "RAG_API_TOKEN is missing; protected requests "
            "will return a configuration error"
        )

    yield

    logger.info("Application shutdown complete")


app = FastAPI(
    title="Production RAG API Learning Example",
    version="1.0.0",
    lifespan=lifespan,
)


# ============================================================
# 6. MOCK RETRIEVAL
# ============================================================

async def retrieve_evidence(
    question: str,
    top_k: int,
) -> list[dict]:
    """
    Simulate a retrieval operation.

    Replace this function with real retrieval from:
    - A vector database.
    - A knowledge graph.
    - A document store.

    In a production implementation, enforce document-level
    access control before returning evidence to the caller.
    """

    # Simulate a small amount of retrieval work.
    await asyncio.sleep(0.05)

    # These passages are examples, not retrieved facts.
    example_evidence = [
        {
            "text": (
                "RAG retrieves relevant source passages and "
                "uses them to support LLM-generated answers."
            ),
            "source_id": "example-doc-1",
        },
        {
            "text": (
                "Retrieval quality affects the evidence "
                "available to the language model."
            ),
            "source_id": "example-doc-2",
        },
        {
            "text": (
                "Citations should point to sources that "
                "support the associated claims."
            ),
            "source_id": "example-doc-3",
        },
    ]

    # The slice enforces the requested maximum.
    return example_evidence[:top_k]


# ============================================================
# 7. MOCK ANSWER GENERATION
# ============================================================

async def generate_answer(
    question: str,
    evidence: list[dict],
) -> str:
    """
    Simulate answer generation without calling an LLM.

    Replace this function with your model client.

    The real implementation should provide selected evidence
    to the model and instruct it not to invent unsupported facts.
    """

    if not evidence:
        return (
            "I could not find sufficient evidence "
            "to answer this question."
        )

    evidence_text = " ".join(
        item["text"]
        for item in evidence
    )

    # This deliberately simple answer shows where the LLM call
    # belongs. It is not a proper grounded answer generator.
    return (
        f"Question received: {question}. "
        f"Retrieved evidence: {evidence_text}"
    )


# ============================================================
# 8. HEALTH ENDPOINT
# ============================================================

@app.get("/health")
async def health():
    """
    Report whether the API process is responding.

    This basic endpoint does not prove that the vector database,
    graph store, or model server is healthy.

    Production systems may expose separate readiness checks
    for required dependencies.
    """

    return {
        "status": "ok",
        "service": "production-rag-learning-example",
    }


# ============================================================
# 9. QUESTION-ANSWERING ENDPOINT
# ============================================================

@app.post(
    "/ask",
    response_model=AskResponse,
    dependencies=[Depends(require_api_token)],
)
async def ask(request: AskRequest):
    """
    Process a question using a simplified RAG workflow.

    Steps:
    1. Create a request ID.
    2. Retrieve evidence with a timeout.
    3. Generate a mock answer.
    4. Collect source identifiers.
    5. Log timing and retrieval statistics.
    6. Return a validated JSON response.
    """

    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        # Step 1: Retrieve evidence.
        # wait_for cancels the awaited operation if it times out.
        evidence = await asyncio.wait_for(
            retrieve_evidence(
                question=request.question,
                top_k=request.top_k,
            ),
            timeout=RETRIEVAL_TIMEOUT_SECONDS,
        )

        # Step 2: Generate the answer.
        answer = await generate_answer(
            question=request.question,
            evidence=evidence,
        )

        # Step 3: Extract source IDs for the response.
        citations = [
            item["source_id"]
            for item in evidence
        ]

        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        # Step 4: Log operational information.
        # Avoid logging private question text or secrets
        # unless there is an approved need and suitable controls.
        logger.info(
            "event=ask_completed request_id=%s "
            "retrieval_count=%d duration_ms=%d",
            request_id,
            len(evidence),
            duration_ms,
        )

        return AskResponse(
            request_id=request_id,
            answer=answer,
            citations=citations,
            retrieval_count=len(evidence),
            duration_ms=duration_ms,
        )

    except asyncio.TimeoutError:
        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        logger.warning(
            "event=retrieval_timeout request_id=%s "
            "duration_ms=%d",
            request_id,
            duration_ms,
        )

        raise HTTPException(
            status_code=504,
            detail={
                "request_id": request_id,
                "error": "Retrieval timed out",
            },
        )

    except HTTPException:
        # Preserve deliberate HTTP errors.
        raise

    except Exception:
        # Log the exception internally without returning
        # sensitive implementation details to the client.
        logger.exception(
            "event=ask_failed request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "error": "An internal error occurred",
            },
        )
```

### Step 3: Configure the API token

In your terminal, run:

```bash
export RAG_API_TOKEN="replace-with-a-long-random-secret"
```

Use a proper secret manager or deployment environment configuration in production.

Do not commit real secrets to Git.

### Step 4: Start the server

Run this command from the repository root:

```bash
uvicorn Practical_exercise.production_rag_api_19:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload
```

If Python cannot import `Practical_exercise.production_rag_api_19`, check the folder structure and run the command from the repository root. You can also run the module from the exercise directory using an appropriate import path.

### Step 5: Test the health endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "production-rag-learning-example"
}
```

### Step 6: Test the question endpoint

```bash
curl -X POST \
  http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer replace-with-a-long-random-secret" \
  -d '{
    "question": "What is RAG?",
    "top_k": 3
  }'
```

The response contains:

- A request ID.
- A simulated answer.
- Source identifiers.
- The number of retrieved passages.
- The processing duration.

The example citations are source IDs, not clickable document URLs. In a real application, return validated source metadata and make sure each citation actually supports the answer.

### Step 7: Test request validation

Try an invalid `top_k` value:

```bash
curl -X POST \
  http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer replace-with-a-long-random-secret" \
  -d '{
    "question": "What is RAG?",
    "top_k": 100
  }'
```

The API should return a validation error because `top_k` must be between 1 and 10.

### What this program teaches

This program is a starting point for learning production API structure. It does not implement a complete production deployment.

For a real system, you would add:

- Actual vector and graph retrieval.
- User identity and document-level authorization.
- Evidence filtering and reranking.
- Real LLM generation.
- Citation verification.
- A shared rate limiter.
- Dependency health checks.
- Metrics and distributed tracing.
- Tests, deployment configuration, and rollback procedures.

---

## 19.6 Practical Exercises

### Exercise 1: Add Request Validation

**Goal:** Learn how to reject invalid API requests before they reach retrieval.

Use the `AskRequest` model in the Python implementation.

Tasks:

1. Send a valid question.
2. Send an empty question.
3. Send a question longer than the configured limit.
4. Set `top_k` to `0`.
5. Set `top_k` to `100`.
6. Observe the API responses.

Expected learning:

Request validation prevents invalid inputs from consuming retrieval and generation resources.

### Exercise 2: Add Document-Level Authorization

**Goal:** Understand why authentication alone is not sufficient.

Create sample documents with access metadata:

```python
documents = [
    {
        "document_id": "public-1",
        "allowed_groups": ["all"],
        "text": "Public company information.",
    },
    {
        "document_id": "engineering-1",
        "allowed_groups": ["engineering"],
        "text": "Engineering team information.",
    },
    {
        "document_id": "hr-1",
        "allowed_groups": ["hr"],
        "text": "Restricted HR information.",
    },
]
```

Tasks:

1. Define test users with different groups.
2. Implement a retrieval filter that uses the authenticated user's trusted groups.
3. Retrieve documents for an engineering user.
4. Retrieve documents for an HR user.
5. Verify that restricted evidence is excluded before prompt construction.
6. Repeat the test with graph retrieval, if available.
7. Verify that citations do not expose restricted documents.

Expected learning:

Permissions must be enforced before private evidence reaches the LLM.

### Exercise 3: Introduce a Retrieval Timeout

**Goal:** Understand timeout handling.

Tasks:

1. Modify `retrieve_evidence()` to wait longer than `RETRIEVAL_TIMEOUT_SECONDS`.
2. Call `/ask`.
3. Observe the timeout response.
4. Restore the normal retrieval delay.
5. Check the logs for the request ID.

Expected learning:

Timeouts prevent a single slow operation from waiting indefinitely.

Important: `asyncio.wait_for()` cancels the awaited coroutine on timeout. It does not guarantee that every external operation has stopped; a database client or remote service may need its own timeout and cancellation handling.

### Exercise 4: Add Index Versioning

**Goal:** Understand how to publish index updates safely.

Suppose your application has:

```python
active_index_version = "index-v1"
```

Tasks:

1. Create a sample `index-v2`.
2. Validate that it contains the expected documents.
3. Simulate a failed validation.
4. Confirm that `index-v1` remains active.
5. Simulate successful validation.
6. Switch the active index to `index-v2`.
7. Record which index version served each test request.

Expected learning:

An index should not become active until it has passed the required validation checks.

In a real multi-worker deployment, store the active version in shared configuration or a registry instead of relying on a local Python variable.

### Exercise 5: Measure Latency

**Goal:** Understand which stages contribute to end-to-end response time.

Measure:

- Query processing.
- Embedding generation.
- Vector retrieval.
- Graph retrieval.
- Reranking.
- LLM generation.
- Citation validation.
- Total request time.

Create a table:

| Operation | Duration (ms) |
|---|---:|
| Query processing | Record your measurement |
| Embedding | Record your measurement |
| Vector retrieval | Record your measurement |
| Graph retrieval | Record your measurement |
| Reranking | Record your measurement |
| LLM generation | Record your measurement |
| Citation validation | Record your measurement |
| Total request | Record your measurement |

Tasks:

1. Run at least 20 representative queries.
2. Record each operation's latency.
3. Calculate p50 and p95 latency.
4. Identify the slowest stage.
5. Optimize that stage and repeat the experiment.

Expected learning:

Performance optimization should be based on measurements rather than assumptions.

### Exercise 6: Compare Vector RAG and Hybrid GraphRAG

**Goal:** Determine when graph retrieval adds value.

Prepare three groups of questions:

- Direct factual questions.
- Relationship and multi-hop questions.
- Broad questions across many documents.

Tasks:

1. Run vector-only retrieval.
2. Run hybrid vector and graph retrieval.
3. Use the same source documents and evaluation questions.
4. Compare evidence relevance.
5. Compare answer correctness and citation support.
6. Measure retrieval latency and total response latency.
7. Record cases where graph retrieval adds no useful evidence.

Expected learning:

GraphRAG adds complexity and cost. Use it when graph relationships or broader graph-level information measurably improve the result.

### Exercise 7: Simulate a Dependency Failure

**Goal:** Learn how to handle unavailable services.

Tasks:

1. Make the mock retrieval function raise an exception.
2. Observe the controlled API error.
3. Add a test for the failure response.
4. Introduce a bounded retry for a simulated transient failure.
5. Verify that invalid requests and authorization failures are not retried unnecessarily.
6. Add a request deadline so retries cannot exceed the overall time budget.

Expected learning:

Retries should be limited to suitable transient failures and must respect timeouts and overall request deadlines.

---

## 19.7 Common Problems

### Problem 1: The Application Rebuilds the Index for Every Question

**Cause:** Indexing and query processing are tightly coupled.

**Solution:**

- Separate offline indexing from online retrieval.
- Store prepared chunks and embeddings.
- Build indexes when the source data changes.
- Use incremental updates where appropriate.

### Problem 2: New Documents Are Not Searchable

**Possible causes:**

- The ingestion job did not run.
- Parsing failed.
- Embedding generation failed.
- The index update was not published.
- The active index version is stale.

**Solution:**

Track document processing status and validate index publication.

### Problem 3: A User Receives Restricted Information

**Cause:** The application retrieves documents without applying the user's permissions.

**Solution:**

- Authenticate the user.
- Derive permissions from trusted identity data.
- Apply access filters to retrieval.
- Check graph traversal and community summaries.
- Prevent cache hits from bypassing authorization.
- Test cross-user information leakage.

### Problem 4: The API Becomes Slow Under Load

**Possible causes:**

- Too many simultaneous LLM requests.
- Expensive graph traversal.
- Slow vector queries.
- Repeated embedding generation.
- An overloaded database.
- Unbounded queues.

**Solution:**

- Measure latency by stage.
- Apply concurrency limits and backpressure.
- Cache safe, reusable results.
- Optimize queries and indexes.
- Scale the actual bottleneck.
- Set realistic timeouts.

### Problem 5: Retries Increase the Load

**Cause:** The system retries failed requests too frequently.

**Solution:**

- Retry only suitable transient failures.
- Use exponential backoff and jitter.
- Limit retry attempts.
- Respect the request deadline.
- Use circuit breakers when appropriate.

### Problem 6: Citations Do Not Support the Answer

**Possible causes:**

- The wrong passages were retrieved.
- The model generated unsupported claims.
- Citations were assigned without verification.
- The underlying document changed.

**Solution:**

- Improve retrieval and ranking.
- Require evidence-grounded generation.
- Validate source references.
- Check important claims against their citations.
- Re-evaluate answers after index updates.

### Problem 7: Index Updates Cause Inconsistent Results

**Cause:** Different workers may use different index versions or a partially updated index.

**Solution:**

- Build and validate a complete new index version.
- Publish it through a controlled version switch.
- Record the active version per request.
- Maintain a rollback path.
- Keep vector, graph, and summary versions compatible.

### Problem 8: Logs Expose Sensitive Information

**Cause:** The application logs tokens, personal information, or full private documents.

**Solution:**

- Log operational metadata instead of sensitive payloads.
- Redact secrets.
- Apply retention and access policies.
- Restrict log access.
- Review whether stored data is necessary.

### Problem 9: The System Works Locally but Fails in Production

**Possible causes:**

- Missing environment variables.
- Incorrect service URLs.
- Different dependencies.
- Invalid credentials.
- Network restrictions.
- Insufficient CPU, memory, or GPU capacity.
- Missing index files or incompatible index versions.

**Solution:**

Use reproducible builds, explicit configuration, startup validation, health checks, deployment tests, and monitored rollouts.

---

## 19.8 Evaluation and Monitoring

Production RAG should be evaluated across quality, latency, reliability, security, and cost.

### 1. Retrieval Quality

Measure whether the retriever returns relevant evidence.

Possible metrics:

- Precision@k.
- Recall@k.
- Mean Reciprocal Rank (MRR).
- Normalized Discounted Cumulative Gain (nDCG).

Use a labeled evaluation dataset when possible.

### 2. Answer Quality

Check whether the final answer is correct and responds to the question.

Possible evaluation dimensions:

- Correctness.
- Completeness.
- Relevance.
- Groundedness.
- Appropriate abstention when evidence is insufficient.

Automated LLM-based evaluation can help, but it should be calibrated against human-reviewed examples.

### 3. Citation Quality

Check whether citations point to real sources and whether those sources support the claims.

Measure:

- Citation validity.
- Citation precision.
- Claim-to-evidence support.
- Citation completeness.

A valid URL does not automatically mean that the cited source supports the answer.

### 4. Latency

Measure end-to-end latency and latency for individual stages.

Common percentiles:

- **p50:** Median response time.
- **p95:** Response time at the 95th percentile.
- **p99:** Response time at the 99th percentile.

Percentiles help reveal slow requests that averages can hide.

### 5. Throughput

Throughput measures how much work the system completes in a given time.

Examples:

- Requests per second.
- Queries per minute.
- Documents indexed per minute.
- Tokens generated per second.

### 6. Reliability

Monitor:

- Request error rate.
- Timeout rate.
- Dependency availability.
- Failed indexing jobs.
- Queue depth.
- Failed index publication.
- Recovery and rollback success.

### 7. Security

Test:

- Authentication failures.
- Authorization enforcement.
- Cross-user cache isolation.
- Restricted document leakage.
- Prompt injection in retrieved content.
- Unauthorized graph traversal.
- Sensitive data in logs.

### 8. Cost

Track:

- Embedding generation.
- LLM input and output tokens.
- Model-serving infrastructure.
- Vector and graph database resources.
- Storage.
- Indexing and summary-generation jobs.

### 9. GraphRAG Evaluation

In addition to ordinary RAG metrics, measure whether graph-based retrieval improves:

- Relationship questions.
- Multi-hop questions.
- Broad collection-level questions.
- Evidence completeness.
- Citation support.

Compare the graph-enabled system with a simpler baseline on the same evaluation dataset.

### Production evaluation table

| Category | What to measure |
|---|---|
| Retrieval | Precision@k, Recall@k, MRR, nDCG |
| Answer quality | Correctness, relevance, groundedness |
| Citations | Validity and claim support |
| Latency | p50, p95, p99 |
| Throughput | Requests and tokens per second |
| Reliability | Errors, timeouts, dependency failures |
| Security | Unauthorized evidence exposure |
| Cost | Model, database, storage, and indexing costs |
| GraphRAG benefit | Improvement over vector-only RAG |

---

## 19.9 Deployment and Scaling

### 1. Separate Services When Necessary

A small application may run the API and retrieval logic in one process.

As the workload grows, it may be useful to separate:

- API service.
- Indexing workers.
- Vector database.
- Graph database.
- Embedding service.
- LLM inference service.
- Monitoring infrastructure.

Do not split every component into a separate service without a clear need. Additional services introduce network calls, operational overhead, and failure modes.

### 2. Use Background Jobs for Indexing

Large document ingestion jobs should generally run outside the normal user request path.

A job queue can coordinate:

1. Document ingestion.
2. Parsing.
3. Chunking.
4. Embedding generation.
5. Graph construction.
6. Validation.
7. Index publication.

Background jobs should be observable and safe to retry.

### 3. Scale Based on the Bottleneck

Different workloads require different scaling strategies.

| Bottleneck | Possible response |
|---|---|
| API CPU usage | Increase worker capacity or optimize processing |
| Vector queries | Improve indexing, filters, or database resources |
| Graph queries | Optimize traversal and graph indexes |
| Embedding generation | Batch requests or scale embedding workers |
| LLM generation | Increase inference capacity or control concurrency |
| Indexing backlog | Scale background workers and inspect slow stages |
| Memory usage | Reduce retained data, bound queues, or increase capacity |

Scaling the API will not necessarily improve performance if the LLM server is the bottleneck.

### 4. Manage Concurrency

The maximum safe concurrency depends on model size, available memory, sequence lengths, KV-cache usage, and request patterns.

For GPU-hosted LLMs, measure:

- Active requests.
- Prompt length.
- Generated token count.
- Queue waiting time.
- GPU memory utilization.
- Tokens per second.
- Time to first token.
- Time between generated tokens.

Do not assume that increasing concurrency always increases throughput.

### 5. Use Health and Readiness Checks

A process can be running while its dependencies are unavailable.

Consider separate checks for:

- Process liveness.
- API readiness.
- Vector database connectivity.
- Graph database connectivity.
- LLM server availability.
- Active index availability.

A liveness check should not repeatedly trigger expensive operations. Readiness checks should verify only the dependencies required for the service to handle traffic.

### 6. Deploy Safely

A typical release procedure is:

1. Run automated tests.
2. Validate configuration.
3. Build the application artifact.
4. Build or select the intended index version.
5. Run smoke tests.
6. Deploy to a limited environment or traffic percentage.
7. Monitor errors, latency, and quality.
8. Expand traffic if healthy.
9. Roll back if the release causes unacceptable problems.

Application rollback and index rollback should both be considered.

---

## 19.10 Key Learnings

After completing this lesson, you should understand:

1. Production RAG separates offline indexing from online question answering.
2. The offline pipeline prepares searchable data, while the online pipeline answers user questions.
3. APIs need request validation, authentication, authorization, and controlled error handling.
4. Authentication identifies users; authorization determines what they can access.
5. Document-level access control must be applied before restricted evidence reaches the LLM.
6. Index versioning and validation make document updates safer.
7. Incremental indexing avoids unnecessary full rebuilds when possible.
8. Caching improves performance but must respect permissions and data freshness.
9. Rate limiting and backpressure protect services from excessive load.
10. Timeouts, bounded retries, and circuit breakers help manage failures.
11. Structured logs, metrics, and distributed traces make production problems easier to diagnose.
12. Evaluation should cover retrieval, answer quality, citation correctness, latency, reliability, security, and cost.
13. GraphRAG adds graph-specific indexing, retrieval, and maintenance requirements.
14. Deployment should include health checks, monitoring, and rollback procedures.
15. Performance decisions should be based on measurements from representative workloads.

**Main takeaway:**

A production RAG or GraphRAG system is a complete software architecture, not just a retrieval function and an LLM. Reliable production systems combine well-designed data pipelines, secure retrieval, grounded generation, monitoring, evaluation, and safe deployment practices.

---

## 19.11 References

### Official documentation

1. **FastAPI — Request Body**

   Learn how to define and validate structured API requests.

   https://fastapi.tiangolo.com/tutorial/body/

2. **FastAPI — Security**

   Learn the security building blocks available in FastAPI.

   https://fastapi.tiangolo.com/tutorial/security/

3. **FastAPI — Handling Errors**

   Learn how to raise and handle HTTP errors.

   https://fastapi.tiangolo.com/tutorial/handling-errors/

4. **OpenTelemetry — Python Documentation**

   Learn how to instrument Python applications for tracing and metrics.

   https://opentelemetry.io/docs/languages/python/

5. **Microsoft GraphRAG — Documentation**

   Learn about GraphRAG indexing, community reports, and query methods.

   https://microsoft.github.io/graphrag/

6. **OWASP — API Security Project**

   Review common API security risks, including authorization failures.

   https://owasp.org/www-project-api-security/

7. **Prometheus — Documentation**

   Learn about metrics collection and monitoring.

   https://prometheus.io/docs/introduction/overview/

### Relevant research

8. Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.*

   Introduces the RAG approach that combines retrieved documents with generation.

   https://arxiv.org/abs/2005.11401

9. Edge et al. (2024), *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.*

   Explores graph-based retrieval and broad questions over document collections.

   https://arxiv.org/abs/2404.16130

---

## Final Practical Checklist

Before moving to the next lesson:

- [ ] Explain the difference between offline indexing and online answering.
- [ ] Run the FastAPI example.
- [ ] Test valid and invalid requests.
- [ ] Test missing and invalid authentication tokens.
- [ ] Simulate a retrieval timeout.
- [ ] Explain why authentication and authorization are different.
- [ ] Describe how index versioning supports rollback.
- [ ] Identify which metrics help diagnose a slow request.
- [ ] Compare vector-only retrieval and hybrid GraphRAG on a small dataset.
- [ ] Explain how you would prevent restricted documents from reaching an LLM.
- [ ] Identify at least three failure modes and their recovery strategies.
- [ ] Describe how to deploy a new application version and index safely.