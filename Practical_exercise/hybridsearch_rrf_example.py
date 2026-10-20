def reciprocal_rank_fusion(
    ranked_lists: list[list[str]],
    k: int = 60,
) -> list[tuple[str, float]]:
    """
    Combine ranked document lists using Reciprocal Rank Fusion.

    Each document is represented by a unique document ID.
    Ranks start at 1.
    """
    if k < 1:
        raise ValueError("k must be at least 1")

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

    return sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0]),
    )


dense_results = ["D1", "D2", "D3"]
sparse_results = ["D3", "D1", "D4"]

combined_results = reciprocal_rank_fusion(
    ranked_lists=[dense_results, sparse_results],
    k=60,
)

print("Combined ranking:")

for rank, (document_id, score) in enumerate(
    combined_results,
    start=1,
):
    print(
        f"{rank}. {document_id} "
        f"(RRF score: {score:.6f})"
    )