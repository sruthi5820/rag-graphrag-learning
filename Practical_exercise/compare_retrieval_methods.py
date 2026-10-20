#13.15 Practical Exercise: Compare Dense, Keyword, and Hybrid Retrieval
#Goal: Implement three retrieval approaches over the same sample documents and compare their returned results for the same questions.
import time

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Sample document collection
# --------------------------------------------------

documents = [
    {
        "id": "D1",
        "text": (
            "AUTH-4017 is an authentication error that can "
            "occur during login."
        ),
        "department": "support",
        "status": "published",
    },
    {
        "id": "D2",
        "text": (
            "To recover account access, follow the account "
            "recovery process and verify your identity."
        ),
        "department": "support",
        "status": "published",
    },
    {
        "id": "D3",
        "text": (
            "Reset a forgotten password to regain access "
            "to your account."
        ),
        "department": "support",
        "status": "published",
    },
    {
        "id": "D4",
        "text": (
            "Python dictionaries store data as key-value "
            "pairs."
        ),
        "department": "engineering",
        "status": "published",
    },
    {
        "id": "D5",
        "text": (
            "The AUTH-4017 troubleshooting guide explains "
            "possible login authentication failures."
        ),
        "department": "support",
        "status": "published",
    },
    {
        "id": "D6",
        "text": (
            "Draft instructions for troubleshooting login "
            "problems before publication."
        ),
        "department": "support",
        "status": "draft",
    },
    {
        "id": "D7",
        "text": (
            "Protect account credentials and enable "
            "available security safeguards."
        ),
        "department": "support",
        "status": "published",
    },
]


# --------------------------------------------------
# 2. Questions and expected relevant document IDs
# --------------------------------------------------

# These expected IDs are manually defined for this
# small educational example.
#
# In a real project, define relevance judgments using
# domain knowledge and representative questions.

test_cases = [
    {
        "question": "How do I fix AUTH-4017?",
        "relevant_ids": {"D1", "D5"},
    },
    {
        "question": "How can I regain access to my account?",
        "relevant_ids": {"D2", "D3"},
    },
    {
        "question": "How do I reset a forgotten password?",
        "relevant_ids": {"D3", "D2"},
    },
]


# --------------------------------------------------
# 3. Prepare the dense retriever
# --------------------------------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

document_texts = [
    document["text"]
    for document in documents
]

document_embeddings = model.encode(
    document_texts,
    normalize_embeddings=True,
)


# --------------------------------------------------
# 4. Prepare the BM25 retriever
# --------------------------------------------------

def tokenize(text: str) -> list[str]:
    """Simple lowercase whitespace tokenization."""
    return text.lower().split()


tokenized_documents = [
    tokenize(document["text"])
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)


# --------------------------------------------------
# 5. Metadata eligibility filter
# --------------------------------------------------

def is_eligible(document: dict) -> bool:
    """
    Only published support documents are eligible
    for this exercise.
    """
    return (
        document["department"] == "support"
        and document["status"] == "published"
    )


eligible_indices = [
    index
    for index, document in enumerate(documents)
    if is_eligible(document)
]


# --------------------------------------------------
# 6. Dense retrieval
# --------------------------------------------------

def dense_search(
    query: str,
    top_k: int = 5,
) -> list[str]:
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    # With normalized embeddings, dot product gives
    # cosine similarity.
    scores = document_embeddings @ query_embedding

    ranked_indices = sorted(
        eligible_indices,
        key=lambda index: float(scores[index]),
        reverse=True,
    )

    return [
        documents[index]["id"]
        for index in ranked_indices[:top_k]
    ]


# --------------------------------------------------
# 7. BM25 keyword retrieval
# --------------------------------------------------

def keyword_search(
    query: str,
    top_k: int = 5,
) -> list[str]:
    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    # Filter eligibility before choosing top results.
    ranked_indices = sorted(
        eligible_indices,
        key=lambda index: float(scores[index]),
        reverse=True,
    )

    # Exclude documents that receive no positive BM25
    # score, rather than returning arbitrary zero-score
    # documents just to fill top_k.
    ranked_indices = [
        index
        for index in ranked_indices
        if scores[index] > 0
    ]

    return [
        documents[index]["id"]
        for index in ranked_indices[:top_k]
    ]


# --------------------------------------------------
# 8. Reciprocal Rank Fusion
# --------------------------------------------------

def reciprocal_rank_fusion(
    ranked_lists: list[list[str]],
    k: int = 60,
) -> list[str]:
    scores: dict[str, float] = {}

    for ranked_list in ranked_lists:
        for rank, document_id in enumerate(
            ranked_list,
            start=1,
        ):
            scores[document_id] = (
                scores.get(document_id, 0.0)
                + 1.0 / (k + rank)
            )

    return [
        document_id
        for document_id, score in sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]


# --------------------------------------------------
# 9. Hybrid retrieval
# --------------------------------------------------

def hybrid_search(
    query: str,
    top_k: int = 5,
) -> list[str]:
    dense_results = dense_search(
        query,
        top_k=top_k,
    )

    keyword_results = keyword_search(
        query,
        top_k=top_k,
    )

    fused_results = reciprocal_rank_fusion(
        [
            dense_results,
            keyword_results,
        ],
        k=60,
    )

    # Final eligibility check.
    eligible_ids = {
        documents[index]["id"]
        for index in eligible_indices
    }

    return [
        document_id
        for document_id in fused_results
        if document_id in eligible_ids
    ][:top_k]


# --------------------------------------------------
# 10. Compare retrieval methods
# --------------------------------------------------

def calculate_recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """
    Recall@k = relevant retrieved documents / all
    known relevant documents for the query.
    """
    if not relevant_ids:
        return 0.0

    retrieved_top_k = set(retrieved_ids[:k])

    relevant_retrieved = (
        retrieved_top_k & relevant_ids
    )

    return len(relevant_retrieved) / len(relevant_ids)


def measure_search(search_function, query: str):
    start_time = time.perf_counter()

    results = search_function(query)

    elapsed_ms = (
        time.perf_counter() - start_time
    ) * 1000

    return results, elapsed_ms


retrievers = {
    "Dense": dense_search,
    "Keyword/BM25": keyword_search,
    "Hybrid": hybrid_search,
}

TOP_K = 3

for test_case in test_cases:
    query = test_case["question"]
    relevant_ids = test_case["relevant_ids"]

    print("\n" + "=" * 70)
    print("Question:", query)
    print("Expected relevant IDs:", sorted(relevant_ids))

    for method_name, search_function in retrievers.items():
        results, latency_ms = measure_search(
            search_function,
            query,
        )

        recall = calculate_recall_at_k(
            retrieved_ids=results,
            relevant_ids=relevant_ids,
            k=TOP_K,
        )

        print(f"\nMethod: {method_name}")
        print(f"Top {TOP_K} results: {results}")
        print(f"Recall@{TOP_K}: {recall:.2f}")
        print(f"Latency: {latency_ms:.2f} ms")