from sentence_transformers import CrossEncoder


query = "How can I recover access to my account?"

documents = [
    {
        "id": "D1",
        "text": (
            "To recover account access, follow the account "
            "recovery instructions and verify your identity."
        ),
    },
    {
        "id": "D2",
        "text": (
            "Python supports lists, dictionaries, loops, "
            "and functions."
        ),
    },
    {
        "id": "D3",
        "text": (
            "If you forget your password, use the password "
            "reset process to regain access."
        ),
    },
    {
        "id": "D4",
        "text": (
            "Account security includes protecting your "
            "credentials and enabling available safeguards."
        ),
    },
]

# This model is downloaded the first time it is used.
# Internet access may be required for the initial download.
model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

pairs = [
    (query, document["text"])
    for document in documents
]

scores = model.predict(pairs)

ranked_documents = sorted(
    zip(documents, scores),
    key=lambda item: float(item[1]),
    reverse=True,
)

print("Query:", query)
print("\nReranked documents:")

for rank, (document, score) in enumerate(
    ranked_documents,
    start=1,
):
    print(f"\nRank: {rank}")
    print("Document ID:", document["id"])
    print("Score:", round(float(score), 4))
    print("Text:", document["text"])