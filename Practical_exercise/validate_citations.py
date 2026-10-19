import re


def extract_citation_ids(answer: str) -> list[str]:
    """Extract unique citation IDs such as [S1] and [S2]."""
    matches = re.findall(r"\[(S\d+)\]", answer)
    return list(dict.fromkeys(matches))


def validate_citation_ids(
    cited_ids: list[str],
    source_records: list[dict],
) -> list[str]:
    """Return citation IDs that exist in the source records."""
    valid_ids = {
        source["source_id"]
        for source in source_records
    }

    return [
        citation_id
        for citation_id in cited_ids
        if citation_id in valid_ids
    ]


sources = [
    {
        "source_id": "S1",
        "text": "RAG retrieves relevant documents for an LLM.",
    },
    {
        "source_id": "S2",
        "text": "Embeddings represent text as vectors.",
    },
]

answer = (
    "RAG retrieves relevant documents for an LLM [S1]. "
    "Embeddings represent text as vectors [S2]. "
    "A third statement refers to a missing source [S3]."
)

cited_ids = extract_citation_ids(answer)

valid_ids = validate_citation_ids(
    cited_ids=cited_ids,
    source_records=sources,
)

invalid_ids = [
    citation_id
    for citation_id in cited_ids
    if citation_id not in valid_ids
]

print("Answer:", answer)
print("Extracted citation IDs:", cited_ids)
print("Valid citation IDs:", valid_ids)
print("Invalid citation IDs:", invalid_ids)