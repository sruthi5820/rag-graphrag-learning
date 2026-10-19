import re


def extract_citation_ids(answer: str) -> list[str]:
    """Extract unique citation IDs from an answer."""
    return list(
        dict.fromkeys(
            re.findall(r"\[(S\d+)\]", answer)
        )
    )


def resolve_citations(
    answer: str,
    source_records: list[dict],
) -> list[dict]:
    """Return source records referenced by valid citation IDs."""
    source_map = {
        source["source_id"]: source
        for source in source_records
    }

    cited_ids = extract_citation_ids(answer)

    return [
        source_map[citation_id]
        for citation_id in cited_ids
        if citation_id in source_map
    ]


sources = [
    {
        "source_id": "S1",
        "title": "RAG Introduction",
        "url": "https://example.org/rag",
        "page": 3,
    },
    {
        "source_id": "S2",
        "title": "Embedding Guide",
        "url": "https://example.org/embeddings",
        "page": 5,
    },
]

answer = (
    "RAG retrieves relevant documents for an LLM [S1]. "
    "Embeddings represent text as numerical vectors [S2]."
)

resolved_sources = resolve_citations(
    answer=answer,
    source_records=sources,
)

for source in resolved_sources:
    page = source.get("page")

    print("\nSource ID:", source["source_id"])
    print("Title:", source["title"])
    print("URL:", source["url"])
    print(
        "Page:",
        page if page is not None else "Not available",
    )