"""
Text File Reading and Chunking

## Objective
Learn how to read a text file, split text into chunks,
assign unique IDs, and save the results as JSON.

## Concepts Learned
- File handling using pathlib
- Reading text with UTF-8 encoding
- Splitting text into words
- Creating chunks of 10 words
- Dictionaries and lists in Python
- Saving data using the JSON module
- Handling FileNotFoundError

## How It Works
1. Read text from sample.txt.
2. Split the text into words.
3. Divide the words into chunks of up to 10 words.
4. Assign each chunk a unique ID.
5. Store each chunk's text and word count.
6. Save the chunks to chunks.json.

## How to Run
python Practical_exercise/chunk_text_01.py

## Expected Result
A chunks.json file containing the generated chunks.

## RAG Connection
Chunking prepares documents for the embedding and retrieval
stages of a RAG pipeline.


"""





import json
from pathlib import Path

# Project root is the directory containing this Python file
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "sample_documents" / "Sample_01.txt"
OUTPUT_FILE = PROJECT_ROOT / "data" / "chunks.json"

CHUNK_SIZE = 10


def read_text(file_path: Path):
    """Read text from a file."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: Input file not found: {file_path}")
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file as UTF-8: {file_path}")
        return None


def split_into_chunks(text: str, chunk_size: int = 10):
    """Split text into chunks containing up to chunk_size words."""
    words = text.split()
    chunks = []

    for start in range(0, len(words), chunk_size):
        chunk_words = words[start:start + chunk_size]

        chunks.append({
            "id": f"chunk_{len(chunks) + 1}",
            "text": " ".join(chunk_words),
            "word_count": len(chunk_words)
        })

    return chunks


def save_chunks(chunks, output_file: Path):
    """Save chunks to a JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=4, ensure_ascii=False)


def main():
    text = read_text(INPUT_FILE)

    if text is None:
        return

    chunks = split_into_chunks(text, CHUNK_SIZE)
    save_chunks(chunks, OUTPUT_FILE)

    print(f"Input file: {INPUT_FILE}")
    print(f"Created {len(chunks)} chunks.")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
