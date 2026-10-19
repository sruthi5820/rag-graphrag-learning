from pathlib import Path
import re


def load_text_file(file_path: Path) -> str:
    """Read a UTF-8 text file."""
    return file_path.read_text(encoding="utf-8")


def clean_text(text: str) -> str:
    """Normalize whitespace without removing meaningful content."""
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def ingest_documents(directory: Path) -> list[dict]:
    """Load, clean, and validate text files."""
    if not directory.is_dir():
        raise NotADirectoryError(
            f"Directory not found: {directory}"
        )

    documents = []

    for file_path in sorted(directory.glob("*.txt")):
        try:
            text = clean_text(load_text_file(file_path))

            if not text:
                print(f"SKIPPED: {file_path.name} is empty")
                continue

            documents.append({
                "filename": file_path.name,
                "source": str(file_path),
                "text": text,
            })

            print(f"SUCCESS: Loaded {file_path.name}")

        except (OSError, UnicodeError) as error:
            print(f"FAILED: {file_path.name}: {error}")

    return documents


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    input_directory = (
        project_root / "data" / "sample_documents"
    )

    documents = ingest_documents(input_directory)

    print(f"\nTotal successfully ingested: {len(documents)}")

    for document in documents:
        print(f"\n--- {document['filename']} ---")
        print(document["text"])