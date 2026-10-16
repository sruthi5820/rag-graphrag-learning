def split_text(text: str, chunk_size: int = 50) -> list[str]:
    """Split text into word-based chunks."""
    words = text.split()

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


document = """
Retrieval-Augmented Generation combines document retrieval
with language generation. It helps a language model use
relevant information from external documents.
"""

chunks = split_text(document, chunk_size=8)

for index, chunk in enumerate(chunks, start=1):
    print(f"Chunk {index}: {chunk}")