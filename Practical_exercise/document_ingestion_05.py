#Load documents, generate metadata, calculate content hashes, and save the processed results to a JSON file.
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json


def create_document_record(file_path: Path) -> dict | None:
    """Load a file and create a record with metadata."""

    try:
        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            print(f"SKIPPED: Empty file: {file_path.name}")
            return None

        content_hash = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

        file_info = file_path.stat()

        return {
            "document_id": content_hash,
            "filename": file_path.name,
            "source": str(file_path.resolve()),
            "file_type": file_path.suffix.lstrip(".").lower(),
            "file_size_bytes": file_info.st_size,
            "updated_at": datetime.fromtimestamp(
                file_info.st_mtime,
                tz=timezone.utc,
            ).isoformat(),
            "content_hash": content_hash,
            "text": text,
        }

    except (OSError, UnicodeError) as error:
        print(f"FAILED: {file_path.name}: {error}")
        return None


def ingest_directory(directory: Path) -> list[dict]:
    """Ingest all text files in a directory."""

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Directory not found: {directory}"
        )

    documents = []

    for file_path in sorted(directory.glob("*.txt")):
        record = create_document_record(file_path)

        if record is not None:
            documents.append(record)

    return documents


def save_as_json(documents: list[dict], output_path: Path) -> None:
    """Save ingested document records to JSON."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Saved {len(documents)} documents to {output_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]

    input_directory = (
        project_root / "data" / "sample_documents"
    )

    output_file = (
        project_root / "data" / "processed_documents.json"
    )

    documents = ingest_directory(input_directory)
    save_as_json(documents, output_file)