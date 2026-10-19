from pathlib import Path


def chunk_text(text: str, chunk_size: int) -> list[str]:
    """Split text into non-overlapping word-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    words = text.split()

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_file = (
        project_root
        / "data"
        / "sample_documents"
        / "chunking_sample.txt"
    )

    if not input_file.is_file():
        raise FileNotFoundError(
            f"Sample document not found: {input_file}"
        )

    text = input_file.read_text(encoding="utf-8").strip()
    words = text.split()

    print(f"Total words: {len(words)}")

    if len(words) < 500:
        raise ValueError(
            "Please expand the sample document to at least 500 words."
        )

    for size in [100, 200, 400]:
        chunks = chunk_text(text, size)

        print(f"\n{'=' * 50}")
        print(f"Chunk size: {size} words")
        print(f"Number of chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks):
            chunk_words = chunk.split()

            print(f"\nChunk {index + 1}")
            print(f"Word count: {len(chunk_words)}")
            print(f"Beginning: {' '.join(chunk_words[:10])}")
            print(f"Ending: {' '.join(chunk_words[-10:])}")


if __name__ == "__main__":
    main()