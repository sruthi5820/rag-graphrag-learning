import hashlib
import json
import re
from pathlib import Path

import networkx as nx
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# =========================================================
# 1. PROJECT PATHS AND SETTINGS
# =========================================================

# Find the project's root directory based on this Python file.
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder containing the original text documents.
DATA_DIR = BASE_DIR / "data" / "sample_documents"

# Folder where the processed JSON files will be saved.
OUTPUT_DIR = BASE_DIR / "data" / "processed"

# Output file paths.
DOCUMENTS_PATH = OUTPUT_DIR / "documents.json"
ENTITIES_PATH = OUTPUT_DIR / "entities.json"
RELATIONSHIPS_PATH = OUTPUT_DIR / "relationships.json"

# Each chunk contains approximately 45 characters.
# The next chunk repeats 8 characters from the previous chunk.
CHUNK_SIZE = 45
CHUNK_OVERLAP = 8


# =========================================================
# 2. DATA MODELS
# =========================================================

# Pydantic models define the structure of our data.
# They also check that the data has the expected types and values.


class Document(BaseModel):
    # Reject fields that are not defined in this model.
    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)


class TextChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    text: str = Field(min_length=1)

    # Character positions of this chunk in the original document.
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)

    # Other names used to refer to the same entity.
    aliases: list[str] = Field(default_factory=list)

    # Documents in which this entity was found.
    source_document_ids: list[str] = Field(default_factory=list)


class Relationship(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # ID of the entity where the relationship starts.
    source_id: str = Field(min_length=1)

    # ID of the entity where the relationship ends.
    target_id: str = Field(min_length=1)

    relationship_type: str = Field(min_length=1)

    # Keep track of where the relationship was found.
    document_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)

    # Original text supporting this relationship.
    evidence: str = Field(min_length=1)

    # A value between 0 and 1.
    confidence: float = Field(ge=0.0, le=1.0)


# =========================================================
# 3. ALLOWED ENTITY AND RELATIONSHIP TYPES
# =========================================================

# These are the entity categories accepted by this example.

ENTITY_TYPES = {
    "PERSON",
    "TECHNOLOGY",
    "PROGRAMMING_LANGUAGE",
    "DATABASE",
    "SOFTWARE_SYSTEM",
}

# These are the relationship categories accepted by this example.

RELATIONSHIP_TYPES = {
    "WORKS_ON",
    "USES",
    "DEVELOPS",
}


# =========================================================
# 4. ENTITY ALIASES
# =========================================================

# Standardize selected names so they use a consistent form.
#
# For example:
# "python" becomes "Python"
# "the rag application" becomes "RAG application"
#
# Only the aliases explicitly listed here are supported.

ALIASES = {
    "rag application": "RAG application",
    "the rag application": "RAG application",
    "python": "Python",
    "chromadb": "ChromaDB",
    "alice": "Alice",
}


# =========================================================
# 5. CREATE SAMPLE DOCUMENTS
# =========================================================

def create_sample_documents() -> None:
    # Create the sample folder if it does not exist.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Two small documents for testing our pipeline.
    samples = {
        "document_001.txt": (
            "Alice develops a RAG application using Python. "
            "The RAG application uses ChromaDB."
        ),
        "document_002.txt": (
            "Alice works on the RAG application. "
            "The application uses Python."
        ),
    }

    for filename, text in samples.items():
        path = DATA_DIR / filename

        # Do not overwrite an existing sample file.
        if not path.exists():
            path.write_text(text, encoding="utf-8")


# =========================================================
# 6. CLEAN TEXT
# =========================================================

def clean_text(text: str) -> str:
    """Remove unnecessary whitespace from text."""

    # Convert Windows and old Mac line endings to standard line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace multiple spaces or tabs with one space.
    text = re.sub(r"[ \t]+", " ", text)

    # Replace three or more consecutive newlines with two.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace at the beginning and end.
    return text.strip()


# =========================================================
# 7. CALCULATE DOCUMENT HASH
# =========================================================

def calculate_hash(text: str) -> str:
    """Create a fingerprint of the document's text."""

    # SHA-256 converts the text into a consistent hexadecimal string.
    # This can help identify whether document content has changed.
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# =========================================================
# 8. LOAD DOCUMENTS
# =========================================================

def load_documents() -> list[Document]:
    documents = []

    # Find every .txt file and process them in sorted order.
    for path in sorted(DATA_DIR.glob("*.txt")):
        raw_text = path.read_text(encoding="utf-8")

        # Clean the text before processing it.
        text = clean_text(raw_text)

        # Skip files that contain no usable text.
        if not text:
            continue

        # Create a validated Document object.
        document = Document(
            document_id=path.stem,
            text=text,
            content_hash=calculate_hash(text),
        )

        documents.append(document)

    return documents


# =========================================================
# 9. SPLIT DOCUMENTS INTO CHUNKS
# =========================================================

def split_into_chunks(
    document: Document,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[TextChunk]:
    """
    Split a document into smaller, overlapping pieces of text.
    """

    # Check that chunk settings are valid.
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size"
        )

    text = document.text
    chunks = []

    start = 0
    index = 1

    # Continue until all document text has been processed.
    while start < len(text):
        # Calculate the end position of the current chunk.
        end = min(start + chunk_size, len(text))

        # If possible, finish at a space instead of splitting a word.
        if end < len(text):
            space = text.rfind(" ", start, end)

            if space > start:
                end = space

        # Extract and clean the current chunk.
        chunk_text = text[start:end].strip()

        if chunk_text:
            # Find the chunk's actual positions in the source text.
            actual_start = text.find(chunk_text, start)
            actual_end = actual_start + len(chunk_text)

            # Create a unique ID for this chunk.
            chunk = TextChunk(
                chunk_id=(
                    f"{document.document_id}_chunk_{index:03d}"
                ),
                document_id=document.document_id,
                text=chunk_text,
                start_char=actual_start,
                end_char=actual_end,
            )

            chunks.append(chunk)
            index += 1

        # Stop when we reach the end of the document.
        if end >= len(text):
            break

        # Move forward while keeping some text from the previous chunk.
        start = max(end - overlap, start + 1)

    return chunks


# =========================================================
# 10. NORMALIZE ENTITY NAMES AND CREATE ENTITY IDS
# =========================================================

def normalize_entity_name(name: str) -> str:
    """Convert supported entity names into a standard form."""

    # Remove extra spaces.
    cleaned = re.sub(r"\s+", " ", name).strip()

    # Ignore capitalization when checking the alias dictionary.
    key = cleaned.casefold()

    # Return the standard name if known.
    # Otherwise, return the cleaned name.
    return ALIASES.get(key, cleaned)


def make_entity_id(name: str, entity_type: str) -> str:
    """Generate a repeatable ID for an entity."""

    # Include the entity type to distinguish different categories.
    key = f"{entity_type}:{name.casefold()}"

    # Create a SHA-256 hash and use the first 12 characters.
    digest = hashlib.sha256(
        key.encode("utf-8")
    ).hexdigest()[:12]

    return f"ent_{digest}"


# =========================================================
# 11. EXTRACT ENTITIES
# =========================================================

def extract_entities(chunk: TextChunk) -> list[dict]:
    """
    Find known entities in a text chunk using regular expressions.

    This is a rule-based example, not a general-purpose extractor.
    """

    text = chunk.text
    found = []

    # Each pattern identifies an entity name and its category.
    patterns = [
        (r"\bAlice\b", "PERSON"),
        (r"\bRAG application\b", "SOFTWARE_SYSTEM"),
        (r"\bPython\b", "PROGRAMMING_LANGUAGE"),
        (r"\bChromaDB\b", "DATABASE"),
    ]

    # Search the text for every defined pattern.
    for pattern, entity_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            name = normalize_entity_name(match.group(0))

            # Keep the entity and its source information.
            found.append({
                "name": name,
                "type": entity_type,
                "document_id": chunk.document_id,
                "chunk_id": chunk.chunk_id,
                "evidence": text,
            })

    return found


# =========================================================
# 12. EXTRACT RELATIONSHIPS
# =========================================================

def extract_relationships(chunk: TextChunk) -> list[dict]:
    """
    Find relationships by matching predefined sentence patterns.
    """

    results = []

    # Split the chunk into sentences using punctuation.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        chunk.text,
    )

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        # Pattern 1:
        # Alice develops a RAG application.
        if re.search(
            r"\bAlice\s+develops?\s+(?:a\s+)?RAG application\b",
            sentence,
            re.IGNORECASE,
        ):
            results.append({
                "source_name": "Alice",
                "source_type": "PERSON",
                "target_name": "RAG application",
                "target_type": "SOFTWARE_SYSTEM",
                "relationship_type": "DEVELOPS",
                "evidence": sentence,
            })

        # Pattern 2:
        # Alice works on the RAG application.
        if re.search(
            r"\bAlice\s+works\s+on\s+(?:the\s+)?RAG application\b",
            sentence,
            re.IGNORECASE,
        ):
            results.append({
                "source_name": "Alice",
                "source_type": "PERSON",
                "target_name": "RAG application",
                "target_type": "SOFTWARE_SYSTEM",
                "relationship_type": "WORKS_ON",
                "evidence": sentence,
            })

        # Pattern 3:
        # The RAG application uses Python or ChromaDB.
        if re.search(
            r"\bRAG application\s+uses\s+(?:the\s+)?"
            r"(?:Python|ChromaDB)\b",
            sentence,
            re.IGNORECASE,
        ):
            # Find which technology is mentioned.
            target_match = re.search(
                r"\b(Python|ChromaDB)\b",
                sentence,
                re.IGNORECASE,
            )

            if target_match:
                target = normalize_entity_name(
                    target_match.group(1)
                )

                # Assign the correct entity category.
                target_type = (
                    "PROGRAMMING_LANGUAGE"
                    if target == "Python"
                    else "DATABASE"
                )

                results.append({
                    "source_name": "RAG application",
                    "source_type": "SOFTWARE_SYSTEM",
                    "target_name": target,
                    "target_type": target_type,
                    "relationship_type": "USES",
                    "evidence": sentence,
                })

        # Pattern 4:
        # The application uses Python.
        #
        # This example treats "the application" as the known
        # RAG application from the sample dataset.
        if re.search(
            r"\bthe application\s+uses\s+(?:the\s+)?Python\b",
            sentence,
            re.IGNORECASE,
        ):
            results.append({
                "source_name": "RAG application",
                "source_type": "SOFTWARE_SYSTEM",
                "target_name": "Python",
                "target_type": "PROGRAMMING_LANGUAGE",
                "relationship_type": "USES",
                "evidence": sentence,
            })

    # Remove duplicate results generated by the same patterns.
    unique = {}

    for item in results:
        key = (
            item["source_name"],
            item["target_name"],
            item["relationship_type"],
            item["evidence"],
        )

        unique[key] = item

    return list(unique.values())


# =========================================================
# 13. MERGE REPEATED ENTITIES
# =========================================================

def build_entity_registry(
    chunks: list[TextChunk],
) -> dict[str, Entity]:
    """
    Create one entity record for each unique entity ID.
    """

    registry = {}

    for chunk in chunks:
        # Extract the entities found in this chunk.
        for item in extract_entities(chunk):
            name = item["name"]
            entity_type = item["type"]

            # Reject entity categories that are not allowed.
            if entity_type not in ENTITY_TYPES:
                raise ValueError(
                    f"Unsupported entity type: {entity_type}"
                )

            # Generate a repeatable ID for this entity.
            entity_id = make_entity_id(name, entity_type)

            # Create the entity the first time it appears.
            if entity_id not in registry:
                registry[entity_id] = Entity(
                    entity_id=entity_id,
                    canonical_name=name,
                    entity_type=entity_type,
                    aliases=[],
                    source_document_ids=[],
                )

            entity = registry[entity_id]

            # Record each source document only once.
            if chunk.document_id not in entity.source_document_ids:
                entity.source_document_ids.append(
                    chunk.document_id
                )

    return registry


# =========================================================
# 14. VALIDATE AND BUILD RELATIONSHIP RECORDS
# =========================================================

def build_relationship_records(
    chunks: list[TextChunk],
    entities: dict[str, Entity],
) -> list[Relationship]:

    records = []

    # Map each entity's name and type to its ID.
    entity_lookup = {
        (
            entity.canonical_name.casefold(),
            entity.entity_type,
        ): entity.entity_id
        for entity in entities.values()
    }

    # Keep track of relationships already added.
    seen = set()

    for chunk in chunks:
        for item in extract_relationships(chunk):
            relationship_type = item["relationship_type"]

            # Check that the relationship type is allowed.
            if relationship_type not in RELATIONSHIP_TYPES:
                raise ValueError(
                    f"Unsupported relationship type: "
                    f"{relationship_type}"
                )

            # Identify the source entity.
            source_key = (
                item["source_name"].casefold(),
                item["source_type"],
            )

            # Identify the target entity.
            target_key = (
                item["target_name"].casefold(),
                item["target_type"],
            )

            # A relationship cannot be created if its source is missing.
            if source_key not in entity_lookup:
                raise ValueError(
                    f"Missing source entity: {source_key}"
                )

            # A relationship cannot be created if its target is missing.
            if target_key not in entity_lookup:
                raise ValueError(
                    f"Missing target entity: {target_key}"
                )

            source_id = entity_lookup[source_key]
            target_id = entity_lookup[target_key]

            # Keep the original sentence as supporting evidence.
            evidence = item["evidence"]

            # Check whether both canonical names appear in the evidence.
            source_present = (
                item["source_name"].casefold()
                in evidence.casefold()
            )

            target_present = (
                item["target_name"].casefold()
                in evidence.casefold()
            )

            # Skip relationships when the required names are absent.
            #
            # Note: "The application uses Python" does not literally
            # contain "RAG application". Therefore, this check skips
            # that relationship even though Pattern 4 found it.
            if not source_present or not target_present:
                continue

            # Create a validated relationship record.
            record = Relationship(
                source_id=source_id,
                target_id=target_id,
                relationship_type=relationship_type,
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                evidence=evidence,
                # This is a demonstration value, not a calibrated score.
                confidence=1.0,
            )

            # Include source details when checking for duplicates.
            key = (
                record.source_id,
                record.target_id,
                record.relationship_type,
                record.document_id,
                record.chunk_id,
                record.evidence,
            )

            if key not in seen:
                records.append(record)
                seen.add(key)

    return records


# =========================================================
# 15. VALIDATE ALL RECORDS
# =========================================================

def validate_records(
    documents: list[Document],
    chunks: list[TextChunk],
    entities: dict[str, Entity],
    relationships: list[Relationship],
) -> None:

    # Store all known document IDs.
    document_ids = {
        document.document_id
        for document in documents
    }

    # Find chunks quickly by their IDs.
    chunk_lookup = {
        chunk.chunk_id: chunk
        for chunk in chunks
    }

    # Store all known entity IDs.
    entity_ids = set(entities)

    # Validate every entity.
    for entity in entities.values():
        if entity.entity_type not in ENTITY_TYPES:
            raise ValueError("Invalid entity type")

        # Every source document must exist.
        for document_id in entity.source_document_ids:
            if document_id not in document_ids:
                raise ValueError(
                    f"Unknown entity source document: {document_id}"
                )

    # Validate every relationship.
    for relationship in relationships:
        if relationship.relationship_type not in RELATIONSHIP_TYPES:
            raise ValueError("Invalid relationship type")

        # Both endpoints must refer to known entities.
        if relationship.source_id not in entity_ids:
            raise ValueError("Unknown source entity ID")

        if relationship.target_id not in entity_ids:
            raise ValueError("Unknown target entity ID")

        # The source document must exist.
        if relationship.document_id not in document_ids:
            raise ValueError("Unknown source document ID")

        # The source chunk must exist.
        if relationship.chunk_id not in chunk_lookup:
            raise ValueError("Unknown source chunk ID")

        chunk = chunk_lookup[relationship.chunk_id]

        # The chunk must belong to the stated document.
        if chunk.document_id != relationship.document_id:
            raise ValueError(
                "Chunk and document provenance do not match"
            )

        # The evidence must actually occur in the chunk.
        if relationship.evidence not in chunk.text:
            raise ValueError(
                "Relationship evidence is not present in its chunk"
            )


# =========================================================
# 16. BUILD THE GRAPH
# =========================================================

def build_graph(
    entities: dict[str, Entity],
    relationships: list[Relationship],
) -> nx.MultiDiGraph:
    """
    Convert entities into graph nodes and relationships into edges.
    """

    # MultiDiGraph supports directed edges and multiple edges
    # between the same pair of nodes.
    graph = nx.MultiDiGraph()

    # Each entity becomes a node.
    for entity in entities.values():
        graph.add_node(
            entity.entity_id,
            name=entity.canonical_name,
            entity_type=entity.entity_type,
        )

    # Each relationship becomes a directed edge.
    for relationship in relationships:
        graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            key=(
                relationship.document_id,
                relationship.chunk_id,
                relationship.relationship_type,
            ),
            relationship_type=relationship.relationship_type,
            document_id=relationship.document_id,
            chunk_id=relationship.chunk_id,
            evidence=relationship.evidence,
            confidence=relationship.confidence,
        )

    return graph


# =========================================================
# 17. SAVE DATA AS JSON
# =========================================================

def save_json(path: Path, value) -> None:
    # Create the output directory if needed.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file first.
    # This helps avoid leaving a partially written final file.
    temporary_path = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary_path.write_text(
        json.dumps(
            value,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Replace the final file after the write completes.
    temporary_path.replace(path)


def save_records(
    documents: list[Document],
    entities: dict[str, Entity],
    relationships: list[Relationship],
) -> None:

    # Convert Pydantic objects into dictionaries before saving.
    save_json(
        DOCUMENTS_PATH,
        [item.model_dump() for item in documents],
    )

    save_json(
        ENTITIES_PATH,
        [item.model_dump() for item in entities.values()],
    )

    save_json(
        RELATIONSHIPS_PATH,
        [item.model_dump() for item in relationships],
    )


# =========================================================
# 18. LOAD SAVED JSON AND VALIDATE ITS STRUCTURE
# =========================================================

def load_and_validate_saved_records():
    # Read the document JSON and recreate Document objects.
    documents = [
        Document.model_validate(item)
        for item in json.loads(
            DOCUMENTS_PATH.read_text(encoding="utf-8")
        )
    ]

    # Read the entity JSON and recreate Entity objects.
    entities_list = [
        Entity.model_validate(item)
        for item in json.loads(
            ENTITIES_PATH.read_text(encoding="utf-8")
        )
    ]

    # Read the relationship JSON and recreate Relationship objects.
    relationships = [
        Relationship.model_validate(item)
        for item in json.loads(
            RELATIONSHIPS_PATH.read_text(encoding="utf-8")
        )
    ]

    # Convert the entity list back into a dictionary indexed by ID.
    entities = {
        entity.entity_id: entity
        for entity in entities_list
    }

    return documents, entities, relationships


# =========================================================
# 19. MAIN PIPELINE
# =========================================================

def main() -> None:
    # Step 1: Create sample files if they do not already exist.
    create_sample_documents()

    # Step 2: Load and clean the source documents.
    documents = load_documents()

    if not documents:
        raise RuntimeError("No source documents were loaded")

    # Step 3: Split each document into chunks.
    chunks = []

    for document in documents:
        chunks.extend(split_into_chunks(document))

    # Step 4: Extract entities and merge repeated mentions.
    entities = build_entity_registry(chunks)

    # Step 5: Extract relationships and validate their evidence.
    relationships = build_relationship_records(
        chunks,
        entities,
    )

    # Step 6: Validate that document, chunk, entity and
    # relationship references are consistent.
    validate_records(
        documents,
        chunks,
        entities,
        relationships,
    )

    # Step 7: Build the directed graph.
    graph = build_graph(
        entities,
        relationships,
    )

    # Step 8: Save documents, entities and relationships as JSON.
    save_records(
        documents,
        entities,
        relationships,
    )

    # Step 9: Read the saved JSON back into Python objects.
    loaded_documents, loaded_entities, loaded_relationships = (
        load_and_validate_saved_records()
    )

    # Step 10: Validate the reloaded records again.
    # The original chunks are used to verify relationship evidence.
    validate_records(
        loaded_documents,
        chunks,
        loaded_entities,
        loaded_relationships,
    )

    # Step 11: Print summary information.
    print("\nDOCUMENT PROCESSING COMPLETE")
    print("-" * 40)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Entities: {len(entities)}")
    print(f"Relationships: {len(relationships)}")
    print(f"Graph nodes: {graph.number_of_nodes()}")
    print(f"Graph edges: {graph.number_of_edges()}")

    # Display all extracted entities.
    print("\nEXTRACTED ENTITIES")

    for entity in entities.values():
        print(
            f"{entity.canonical_name} "
            f"({entity.entity_type}) "
            f"[{entity.entity_id}]"
        )

    # Display all extracted relationships and their evidence.
    print("\nEXTRACTED RELATIONSHIPS")

    for relationship in relationships:
        source = entities[
            relationship.source_id
        ].canonical_name

        target = entities[
            relationship.target_id
        ].canonical_name

        print(
            f"{source} "
            f"--{relationship.relationship_type}--> "
            f"{target}"
        )

        print(f"  Evidence: {relationship.evidence}")

        print(
            f"  Source: {relationship.document_id}, "
            f"{relationship.chunk_id}"
        )

    # Show where the JSON files were saved.
    print("\nSAVED FILES")
    print(DOCUMENTS_PATH)
    print(ENTITIES_PATH)
    print(RELATIONSHIPS_PATH)

    print("\nReload and validation successful.")


# =========================================================
# 20. START THE PROGRAM
# =========================================================

if __name__ == "__main__":
    try:
        # Run the entire pipeline when this file is executed directly.
        main()

    except (ValueError, ValidationError) as exc:
        # Display a readable error if validation fails.
        raise SystemExit(
            f"Validation failed: {exc}"
        ) from exc