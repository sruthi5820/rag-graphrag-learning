documents = [
    {
        "id": "D1",
        "text": "Support account recovery instructions.",
        "department": "support",
        "status": "published",
    },
    {
        "id": "D2",
        "text": "Employee leave policy.",
        "department": "hr",
        "status": "published",
    },
    {
        "id": "D3",
        "text": "Draft support troubleshooting guide.",
        "department": "support",
        "status": "draft",
    },
    {
        "id": "D4",
        "text": "Published login troubleshooting guide.",
        "department": "support",
        "status": "published",
    },
]


def filter_documents(
    documents: list[dict],
    department: str,
    status: str,
) -> list[dict]:
    """Return documents matching both metadata conditions."""
    return [
        document
        for document in documents
        if document.get("department") == department
        and document.get("status") == status
    ]


eligible_documents = filter_documents(
    documents=documents,
    department="support",
    status="published",
)

print("Eligible documents:")

for document in eligible_documents:
    print("\nID:", document["id"])
    print("Text:", document["text"])
    print("Department:", document["department"])
    print("Status:", document["status"])