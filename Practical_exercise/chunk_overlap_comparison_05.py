from pathlib import Path


def chunk_text(
    text: str,
    chunk_size: int,
    overlap: int,
) -> list[str]:
    """Split text into word-based chunks with overlap."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and < chunk_size"
        )

    words = text.split()
    step = chunk_size - overlap

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), step)
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

    chunk_size = 200

    for overlap in [0, 20, 40]:
        chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        overlap_percentage = overlap / chunk_size * 100

        total_chunk_words = sum(
            len(chunk.split()) for chunk in chunks
        )

        print(f"\n{'=' * 50}")
        print(f"Chunk size: {chunk_size}")
        print(f"Overlap: {overlap}")
        print(f"Overlap percentage: {overlap_percentage:.0f}%")
        print(f"Number of chunks: {len(chunks)}")
        print(f"Total words across chunks: {total_chunk_words}")

        for index, chunk in enumerate(chunks):
            chunk_words = chunk.split()

            print(f"\nChunk {index + 1}")
            print(f"Word count: {len(chunk_words)}")
            print(f"Beginning: {' '.join(chunk_words[:10])}")
            print(f"Ending: {' '.join(chunk_words[-10:])}")

            if index < len(chunks) - 1:
                next_words = chunks[index + 1].split()

                actual_overlap = 0
                max_possible = min(
                    len(chunk_words),
                    len(next_words),
                    overlap,
                )

                for count in range(max_possible, 0, -1):
                    if chunk_words[-count:] == next_words[:count]:
                        actual_overlap = count
                        break

                print(
                    f"Repeated words with next chunk: "
                    f"{actual_overlap}"
                )


if __name__ == "__main__":
    main()