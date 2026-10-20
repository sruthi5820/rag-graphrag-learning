import json
import time
from pathlib import Path


DATASET_PATH = Path("data/rag_evaluation_dataset.json")


def load_dataset() -> list[dict]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def mock_retrieve(question: str) -> list[str]:
    """
    Replace this function with your real retriever.

    Return ranked document IDs.
    """
    if "password" in question.lower():
        return ["doc-001", "doc-004", "doc-010"]

    return []


def mock_generate(
    question: str,
    retrieved_source_ids: list[str],
) -> str:
    """
    Replace this function with your actual LLM generation call.
    """
    if not retrieved_source_ids:
        return (
            "The available documents do not provide "
            "enough information to answer this question."
        )

    return (
        "Follow the documented password recovery procedure. "
        "[doc-001]"
    )


def recall_at_k(
    expected_ids: list[str],
    retrieved_ids: list[str],
    k: int = 5,
) -> float | None:
    expected = set(expected_ids)

    if not expected:
        return None

    retrieved = set(retrieved_ids[:k])

    return len(expected & retrieved) / len(expected)


def exact_match(
    generated: str,
    expected: str,
) -> float:
    normalize = lambda text: " ".join(text.lower().split())

    return float(normalize(generated) == normalize(expected))


def evaluate_record(record: dict) -> dict:
    start = time.perf_counter()

    question = record["question"]
    expected_ids = record["expected_source_ids"]
    expected_answer = record["expected_answer"]
    category = record["category"]

    retrieval_start = time.perf_counter()
    retrieved_ids = mock_retrieve(question)
    retrieval_latency_ms = (
        time.perf_counter() - retrieval_start
    ) * 1000

    answer_start = time.perf_counter()
    answer = mock_generate(question, retrieved_ids)
    generation_latency_ms = (
        time.perf_counter() - answer_start
    ) * 1000

    total_latency_ms = (time.perf_counter() - start) * 1000

    return {
        "question": question,
        "category": category,
        "retrieved_source_ids": retrieved_ids,
        "answer": answer,
        "recall_at_5": recall_at_k(
            expected_ids,
            retrieved_ids,
        ),
        "exact_match": exact_match(
            answer,
            expected_answer,
        ),
        "retrieval_latency_ms": round(
            retrieval_latency_ms, 2
        ),
        "generation_latency_ms": round(
            generation_latency_ms, 2
        ),
        "total_latency_ms": round(
            total_latency_ms, 2
        ),
    }


def main():
    dataset = load_dataset()

    results = [
        evaluate_record(record)
        for record in dataset
    ]

    output_path = Path("data/rag_evaluation_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print(f"Evaluated {len(results)} questions.")
    print(f"Results saved to: {output_path}")

    for result in results:
        recall = result["recall_at_5"]

        recall_text = (
            "N/A"
            if recall is None
            else f"{recall:.2%}"
        )

        print()
        print("Question:", result["question"])
        print("Category:", result["category"])
        print("Recall@5:", recall_text)
        print("Exact match:", result["exact_match"])
        print("Total latency:", result["total_latency_ms"], "ms")


if __name__ == "__main__":
    main()