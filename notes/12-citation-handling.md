
# Lesson 12: Citation Handling in RAG


## 12.1 What Is a Citation?

A citation identifies the source that supports a statement in a generated answer.

In a RAG application, a citation may point to:

- A document.
- A webpage.
- A PDF page.
- A particular passage or chunk.
- A section of a document.

Citations allow users to trace an answer back to its supporting evidence.

### Example

Retrieved source:

```text
Source ID: S1
Text: Embeddings represent text as numerical vectors.
URL: https://example.org/embeddings
Page: 5
```

User question:

"What are embeddings?"

Generated answer:

"Embeddings represent text as numerical vectors [S1]."

Here, `[S1]` is a citation reference. The application can use that ID to find the actual source record and display its link and page number.

The example URL is illustrative and is not a real evidence source.

### Why Are Citations Important?

Citations help users:

1. Verify information in the original source.
2. Understand where a claim came from.
3. Investigate a statement in more detail.
4. Identify which documents support an answer.
5. Detect answers that lack supporting evidence.
6. Build trust through transparent sourcing.

### Important Principle

A citation is useful only when it points to a real source that supports the associated claim.

A reference that merely exists in the database is not necessarily a correct citation.

---

## 12.2 Source, Chunk, and Citation

These three terms are related but have different meanings.

### Source

A source is the original information resource.

Examples:

- A PDF document.
- A webpage.
- A technical manual.
- A report.
- A knowledge-base article.

### Chunk

A chunk is a smaller piece of text taken from a source.

A single document may contain many chunks.

For example:

```text
Document: embeddings-guide.pdf

Chunk 1: What embeddings represent.
Chunk 2: How embeddings are generated.
Chunk 3: How vector similarity works.
```

### Citation

A citation is a reference connecting a statement in an answer to a supporting source or passage.

For example:

```text
Answer:
Embeddings represent text as numerical vectors [S2].
```

The application maps `[S2]` to a stored source record.

### Comparison

| Term | Meaning | Example |
|---|---|---|
| Source | Original information resource | embeddings-guide.pdf |
| Chunk | Part of the source text | Explanation on page 5 |
| Citation | Reference supporting an answer claim | [S2] |

### Why This Difference Matters

A citation system needs enough information to connect a generated answer to the correct source.

If the application retrieves chunk text but loses the original document URL or page number, it may be unable to provide a useful source reference.

---

## 12.3 Citation Handling Workflow

A basic citation workflow consists of these steps:

1. Retrieve relevant chunks.
2. Preserve the metadata associated with each chunk.
3. Assign or retain a source ID.
4. Pass the source IDs and chunk content to the LLM.
5. Generate an answer that references those IDs.
6. Extract the citation IDs from the answer.
7. Validate the IDs against the sources actually supplied.
8. Map valid IDs to source URLs, titles, and page numbers.
9. Display the answer with its source references.

### Workflow Diagram

```text
Retrieved Chunks
       |
       v
Preserve Source Metadata
       |
       v
Assign Source IDs
       |
       v
Provide Sources to LLM
       |
       v
Generate Answer with References
       |
       v
Extract and Validate Reference IDs
       |
       v
Map IDs to Source Links
       |
       v
Return Answer with Citations
```

### Example

Suppose the retrieval system returns two chunks:

```python
sources = [
    {
        "source_id": "S1",
        "text": "RAG retrieves relevant documents for an LLM.",
        "url": "https://example.org/rag-guide",
        "page": 3,
    },
    {
        "source_id": "S2",
        "text": "Embeddings represent text as vectors.",
        "url": "https://example.org/embeddings",
        "page": 5,
    },
]
```

The LLM receives the text with its corresponding source IDs.

It may generate:

```text
RAG retrieves relevant documents for an LLM [S1].
Embeddings represent text as vectors [S2].
```

The application then maps `[S1]` and `[S2]` to their corresponding source records.

**Important:** The URLs in this example are placeholders for learning. They should not be presented as real sources.

---

## 12.4 Source IDs

A source ID is a unique identifier used to refer to a source record.

Examples:

```text
S1
S2
S3
```

Source IDs make it easier for the model to refer to evidence without reproducing complete URLs.

### Example Source Records

```python
sources = [
    {
        "source_id": "S1",
        "title": "RAG Introduction",
        "text": "RAG retrieves relevant information for an LLM.",
        "url": "https://example.org/rag",
        "page": 3,
    },
    {
        "source_id": "S2",
        "title": "Embedding Guide",
        "text": "Embeddings represent text as numerical vectors.",
        "url": "https://example.org/embeddings",
        "page": 5,
    },
]
```

Each record contains:

- `source_id`: identifier used in the answer.
- `title`: readable source title.
- `text`: retrieved evidence.
- `url`: source location.
- `page`: page number, when applicable.

### Why Use Source IDs?

Source IDs help the application:

- Connect claims to source records.
- Avoid relying on URLs invented by the model.
- Validate references.
- Render links consistently.
- Identify which sources were supplied for a particular answer.

### Source ID Requirements

A good source ID should be:

1. Unique within the relevant answer or source set.
2. Stable while the answer is being processed.
3. Connected to an actual retrieved record.
4. Easy to validate.
5. Separate from the document's display title or URL.

For a simple exercise, IDs such as `S1` and `S2` are sufficient.

For larger applications, persistent chunk IDs or document IDs may be used internally, while short answer-specific citation labels are generated for display.

---

## 12.5 Preserving Source Metadata

Citation handling depends on preserving metadata from the original source.

Useful fields include:

| Field | Purpose |
|---|---|
| `source_id` | Reference used by the answer |
| `document_id` | Identifies the original document |
| `chunk_id` | Identifies a particular chunk |
| `title` | Human-readable document title |
| `url` | Link to the source |
| `page` | Page number for paginated documents |
| `section` | Section or heading, if available |
| `text` | Retrieved evidence |

Not every source has every field. For example, a webpage may not have meaningful page numbers.

### Example

```python
source = {
    "source_id": "S1",
    "document_id": "doc_001",
    "chunk_id": "chunk_003",
    "title": "Embedding Guide",
    "url": "https://example.org/embeddings",
    "page": 5,
    "section": "What Are Embeddings?",
    "text": "Embeddings represent text as numerical vectors.",
}
```

### Why Metadata Must Be Preserved

Suppose the application retrieves a useful chunk but keeps only its text:

```python
chunk_text = "Embeddings represent text as numerical vectors."
```

The application can display the text, but it may not know which document, URL, or page supports it.

Instead, retain the text and its associated source metadata together.

### Practical Rule

Do not separate a chunk from the source information needed to identify its origin.

---

## 12.6 Citation Formats

Citations can be displayed in different formats depending on the application.

### Format 1: Source IDs

```text
Embeddings represent text as numerical vectors [S1].
```

Advantages:

- Simple to generate.
- Easy to validate.
- Easy to map to source records.

### Format 2: Numbered References

```text
Embeddings represent text as numerical vectors [1].
```

The application maps `[1]` to the first source in the reference list.

If the source order changes, the mapping must be updated accordingly.

### Format 3: Inline Links

```text
Embeddings represent text as numerical vectors.
```

The application attaches a link to the appropriate phrase or citation marker.

This format requires the application to map the claim or marker to the correct source URL.

### Format 4: Document and Page

```text
Embeddings represent text as numerical vectors
(Embedding Guide, page 5).
```

This is useful when users need to locate evidence inside a long PDF or document.

### Choosing a Format

The best format depends on the application and its users.

For this lesson, use source IDs such as `[S1]` and `[S2]`, because they are easy to implement and validate in Python.

---

## 12.7 Generating Answers with Source IDs

The model should receive each source ID alongside the relevant text.

Example:

```text
Source [S1]:
RAG retrieves relevant documents for an LLM.

Source [S2]:
Embeddings represent text as numerical vectors.

Question:
What are RAG and embeddings?

Answer:
```

The model may then produce:

```text
RAG retrieves relevant documents for an LLM [S1].
Embeddings represent text as numerical vectors [S2].
```

The application should resolve each ID using the source records that were actually supplied.

### Why This Is Better Than Asking the Model to Invent URLs

A model may generate an incorrect URL or refer to a document that was never retrieved.

With source IDs, the application can validate whether a reference belongs to the supplied source set.

### Important Rule

The application, not the LLM, should determine the final URL and page information by looking up the validated source record.

The model's output is a proposed reference, not proof that the source exists or supports the claim.

---

## 12.8 Citation Validation

Citation validation checks whether the references generated by the model correspond to real source records.

Consider this answer:

```text
Embeddings represent text as numerical vectors [S2].
Vector databases search for similar vectors [S3].
```

Suppose the application supplied only `[S1]` and `[S2]`.

The reference `[S3]` is invalid because it does not exist in the supplied source set.

### Basic Validation Function

```python
def validate_citation_ids(
    cited_ids: list[str],
    source_records: list[dict],
) -> list[str]:
    """Return citation IDs that exist in the supplied sources."""

    valid_ids = {
        source["source_id"]
        for source in source_records
    }

    return [
        citation_id
        for citation_id in cited_ids
        if citation_id in valid_ids
    ]
```

### Example

```python
sources = [
    {
        "source_id": "S1",
        "text": "RAG retrieves relevant documents for an LLM.",
        "url": "https://example.org/rag",
    },
    {
        "source_id": "S2",
        "text": "Embeddings represent text as vectors.",
        "url": "https://example.org/embeddings",
    },
]

cited_ids = ["S1", "S2", "S3"]

valid_ids = validate_citation_ids(
    cited_ids=cited_ids,
    source_records=sources,
)

print("Valid citation IDs:", valid_ids)
```

Expected output:

```text
Valid citation IDs: ['S1', 'S2']
```

### Important Limitation

This function validates that an ID exists in the supplied source set.

It does not prove that the cited source supports the statement.

For example, `[S1]` might be a valid ID but contain no information about the claim that follows it.

**Citation ID validation and claim-support validation are separate tasks.**

---

## 12.9 Extracting Citation IDs from an Answer

Before validating citation IDs, the application needs to identify the references in the generated answer.

Python's regular expressions can extract IDs in a format such as `[S1]`.

```python
import re


def extract_citation_ids(answer: str) -> list[str]:
    """Extract source IDs such as S1 from [S1] markers."""

    matches = re.findall(
        r"\[(S\d+)\]",
        answer,
    )

    # Remove duplicate IDs while preserving their order.
    return list(dict.fromkeys(matches))


answer = (
    "RAG retrieves relevant documents for an LLM [S1]. "
    "Embeddings represent text as vectors [S2]."
)

citation_ids = extract_citation_ids(answer)

print(citation_ids)
```

Expected output:

```text
['S1', 'S2']
```

### How It Works

The regular expression:

```python
r"\[(S\d+)\]"
```

matches a pattern consisting of:

- An opening square bracket.
- The letter `S`.
- One or more digits.
- A closing square bracket.

It matches `[S1]` and `[S25]`.

It does not match every possible citation format. If your application uses different IDs, update the extraction pattern accordingly.

---

## 12.10 Mapping Citations to Source Links

After validating citation IDs, the application can map them to the corresponding source metadata.

```python
def get_sources_for_citations(
    cited_ids: list[str],
    source_records: list[dict],
) -> list[dict]:
    """Return source records referenced by valid citation IDs."""

    source_map = {
        source["source_id"]: source
        for source in source_records
    }

    resolved_sources = []

    for citation_id in cited_ids:
        source = source_map.get(citation_id)

        if source is not None:
            resolved_sources.append(source)

    return resolved_sources
```

### Example

```python
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

cited_ids = ["S2", "S1"]

resolved = get_sources_for_citations(
    cited_ids=cited_ids,
    source_records=sources,
)

for source in resolved:
    print(
        source["source_id"],
        source["title"],
        source["url"],
        source.get("page"),
    )
```

The application retrieves the source details from its own records instead of trusting a URL generated by the model.

### Security Consideration

A real application should also apply its URL and access-control policies before displaying links. Validating a citation ID does not automatically make every destination safe or accessible to every user.

---

## 12.11 Citation Granularity

Citation granularity refers to how specifically a citation identifies the supporting evidence.

### Document-Level Citation

The citation points to an entire document.

Example:

```text
Embeddings represent text as numerical vectors [S1].
```

Here, `[S1]` might identify an entire document about embeddings.

### Page-Level Citation

The citation points to a particular page.

Example:

```text
Embeddings represent text as numerical vectors
(Embedding Guide, page 5).
```

### Chunk- or Passage-Level Citation

The citation identifies a particular passage within a document.

This can make it easier for the reader to locate the exact supporting information.

### Comparison

| Granularity | Reference | Main benefit |
|---|---|---|
| Document | Whole document | Simple to implement |
| Page | Specific page | Easier to locate information in PDFs |
| Passage | Specific text segment | More precise evidence tracing |

### Practical Principle

Use the most specific reference your application can reliably preserve.

Do not invent page numbers or passage locations when they are not available.

---

## 12.12 Multiple Claims and Multiple Citations

An answer may contain more than one factual statement.

Different statements may require different sources.

### Example

Source S1:

"RAG retrieves relevant documents for an LLM."

Source S2:

"Embeddings represent text as numerical vectors."

Question:

"What do RAG and embeddings do?"

Appropriate answer:

"RAG retrieves relevant documents for an LLM [S1]. Embeddings represent text as numerical vectors [S2]."

Each citation is placed near the statement it supports.

### Why Placement Matters

If an answer contains five claims and puts one citation only at the end, the reader may not know which claims the source supports.

For clear attribution:

- Place the reference near the supported claim.
- Use multiple source IDs when several sources support a statement.
- Avoid attaching a source to unrelated claims.
- Do not assume that one citation supports every sentence in a paragraph.

A source may support some statements in an answer without supporting all of them.

---

## 12.13 Unsupported Claims and Missing Citations

A generated answer may contain a statement without a citation.

Example:

```text
Embeddings represent text as numerical vectors [S2].
The most accurate embedding model is Model X.
```

Suppose the retrieved sources contain no comparison of embedding-model accuracy.

The second statement is unsupported by the supplied evidence, even if the model happens to know a model by that name.

### Possible Problems

- A factual statement has no citation.
- A citation refers to an unrelated source.
- A source ID does not exist.
- The cited document does not support the claim.
- A citation points to a document but not the relevant page.
- The answer makes a claim that is absent from all supplied sources.

### Basic Application Rules

A citation-handling implementation should:

1. Extract generated citation IDs.
2. Check that every ID exists in the supplied source set.
3. Resolve IDs using the original source metadata.
4. Avoid displaying invalid references as verified links.
5. Check whether the evidence actually supports the associated claim.
6. Define how the application handles unsupported statements.

For this lesson, manually inspect whether citations support their claims. More comprehensive automated evaluation belongs in the separate RAG evaluation lesson.

---

## 12.14 Handling Questions with No Supporting Source

A question may ask for information that is absent from the retrieved documents.

Example source:

```text
Source ID: S1
Text: Embeddings represent text as numerical vectors.
```

Question:

"What is the population of Tokyo?"

The source does not provide the population of Tokyo.

The answer should not invent a population figure and cite `[S1]`.

### Expected Behavior

The application should acknowledge that the available source does not answer the question.

For example:

"The supplied source explains embeddings but does not contain information about Tokyo's population."

### What Should the Citation System Do?

- Do not invent a source ID.
- Do not attach an unrelated citation to the answer.
- Do not display a citation as evidence for a claim it does not support.
- Preserve the distinction between valid source references and supported factual claims.

A source ID can be valid while the answer itself is unsupported. Both questions must be considered separately.

---

## 12.15 Common Citation Handling Mistakes

### Mistake 1: Trusting Model-Generated URLs

The model may output a URL that was never retrieved.

**Better approach:** Generate source references from the actual source records.

### Mistake 2: Accepting Any Citation ID

The answer might contain `[S9]` even though only `[S1]` and `[S2]` were supplied.

**Better approach:** Validate all cited IDs against the supplied source set.

### Mistake 3: Treating a Valid ID as Proof

A valid ID does not guarantee that the cited passage supports the statement.

**Better approach:** Inspect the claim and the cited evidence together.

### Mistake 4: Losing Source Metadata

If source URLs and page numbers are discarded, the application may not be able to produce useful links.

**Better approach:** Preserve the original source metadata alongside each retrieved chunk.

### Mistake 5: Inventing Page Numbers

A model may produce a page number that does not exist in the source record.

**Better approach:** Use only page information preserved from the actual source.

### Mistake 6: Putting One Citation at the End of Every Answer

A citation at the end of a long answer may not clearly support every statement.

**Better approach:** Associate citations with the claims they support.

### Mistake 7: Citing an Unrelated Source

The model may select a valid source ID that does not support the claim.

**Better approach:** Check claim-level evidence, not just ID validity.

### Mistake 8: Treating Citation Presence as Guaranteed Correctness

An answer may contain many citations and still be inaccurate.

**Better approach:** Verify the relationship between each claim and its supporting source.

---

## 12.16 Practical Exercise 1: Attach Source IDs to Chunks

### Goal

Create source records that preserve the connection between text and its origin.

### Task

Create the file:

`Practical_exercise/citation_source_records.py`

```python
sources = [
    {
        "source_id": "S1",
        "document_id": "doc_001",
        "chunk_id": "chunk_001",
        "title": "RAG Introduction",
        "text": "RAG retrieves relevant documents for an LLM.",
        "url": "https://example.org/rag",
        "page": 3,
    },
    {
        "source_id": "S2",
        "document_id": "doc_002",
        "chunk_id": "chunk_002",
        "title": "Embedding Guide",
        "text": "Embeddings represent text as numerical vectors.",
        "url": "https://example.org/embeddings",
        "page": 5,
    },
]

for source in sources:
    print("\nSource ID:", source["source_id"])
    print("Document ID:", source["document_id"])
    print("Chunk ID:", source["chunk_id"])
    print("Title:", source["title"])
    print("Text:", source["text"])
    print("URL:", source["url"])
    print("Page:", source["page"])
```

### Run the exercise

```bash
python Practical_exercise/citation_source_records.py
```

### Questions

1. Why does each record need a source ID?
2. Why should the URL and page number be preserved?
3. What problem occurs if the text is stored without its source metadata?
4. How would you represent a webpage that has no page number?

---

## 12.17 Practical Exercise 2: Extract and Validate Citation IDs

### Goal

Extract source references from a generated answer and reject references that do not exist in the supplied source set.

### File

`Practical_exercise/validate_citations.py`

```python
import re


def extract_citation_ids(answer: str) -> list[str]:
    """Extract source IDs such as S1 from [S1] markers."""

    matches = re.findall(r"\[(S\d+)\]", answer)

    return list(dict.fromkeys(matches))


def validate_citation_ids(
    cited_ids: list[str],
    source_records: list[dict],
) -> list[str]:
    """Return IDs that exist in the supplied source records."""

    valid_ids = {
        source["source_id"]
        for source in source_records
    }

    return [
        citation_id
        for citation_id in cited_ids
        if citation_id in valid_ids
    ]


sources = [
    {
        "source_id": "S1",
        "text": "RAG retrieves relevant documents for an LLM.",
    },
    {
        "source_id": "S2",
        "text": "Embeddings represent text as vectors.",
    },
]

answer = (
    "RAG retrieves relevant documents for an LLM [S1]. "
    "Embeddings represent text as vectors [S2]. "
    "A third statement refers to a missing source [S3]."
)

cited_ids = extract_citation_ids(answer)

valid_ids = validate_citation_ids(
    cited_ids=cited_ids,
    source_records=sources,
)

invalid_ids = [
    citation_id
    for citation_id in cited_ids
    if citation_id not in valid_ids
]

print("Answer:", answer)
print("Extracted citation IDs:", cited_ids)
print("Valid citation IDs:", valid_ids)
print("Invalid citation IDs:", invalid_ids)
```

### Run the exercise

```bash
python Practical_exercise/validate_citations.py
```

### Expected output

```text
Extracted citation IDs: ['S1', 'S2', 'S3']
Valid citation IDs: ['S1', 'S2']
Invalid citation IDs: ['S3']
```

### Questions

1. Why is `[S3]` invalid?
2. Does `[S1]` being valid prove that the first claim is supported?
3. What should the application do with invalid references?
4. How would you change the code if your citation format used `[1]`, `[2]`, and `[3]`?

---

## 12.18 Practical Exercise 3: Map Citation IDs to Source Links

### Goal

Resolve valid citation IDs to their actual source metadata.

### File

`Practical_exercise/resolve_citations.py`

```python
import re


def extract_citation_ids(answer: str) -> list[str]:
    return list(
        dict.fromkeys(
            re.findall(r"\[(S\d+)\]", answer)
        )
    )


def resolve_citations(
    answer: str,
    source_records: list[dict],
) -> list[dict]:
    """Return the source records referenced by valid IDs."""

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

    print("Source ID:", source["source_id"])
    print("Title:", source["title"])
    print("URL:", source["url"])
    print("Page:", page if page is not None else "Not available")
```

### Run the exercise

```bash
python Practical_exercise/resolve_citations.py
```

### Questions

1. How does the source map connect IDs to records?
2. Why should the application use the stored URL rather than a URL generated by the LLM?
3. What happens when a cited ID is missing?
4. How could the application display a page number when it is available?

The URLs in this exercise are illustrative placeholders.

---

## 12.19 Practical Exercise 4: Check Whether a Citation Supports a Claim

### Goal

Distinguish a citation that exists from a citation that actually supports the associated statement.

### Task

Create:

`Practical_exercise/check_citation_support.py`

```python
sources = [
    {
        "source_id": "S1",
        "text": "RAG retrieves relevant documents for an LLM.",
    },
    {
        "source_id": "S2",
        "text": "Embeddings represent text as numerical vectors.",
    },
]

claims = [
    {
        "claim": "RAG retrieves relevant documents for an LLM.",
        "citation_ids": ["S1"],
    },
    {
        "claim": "Embeddings represent text as numerical vectors.",
        "citation_ids": ["S2"],
    },
    {
        "claim": "The most accurate embedding model is Model X.",
        "citation_ids": ["S2"],
    },
]

source_map = {
    source["source_id"]: source["text"]
    for source in sources
}

for item in claims:
    print("\nClaim:", item["claim"])

    for citation_id in item["citation_ids"]:
        source_text = source_map.get(citation_id)

        if source_text is None:
            print(f"{citation_id}: INVALID SOURCE ID")
        else:
            print(f"{citation_id}: Valid source ID")
            print("Source text:", source_text)

    print(
        "Manual check required: Does the source text "
        "actually support the claim?"
    )
```

### Run the exercise

```bash
python Practical_exercise/check_citation_support.py
```

### Task

For each claim, determine whether the associated source text actually supports it.

| Claim | Citation ID valid? | Claim supported? | Explanation |
|---|---|---|---|
| RAG retrieves relevant documents for an LLM. | | | |
| Embeddings represent text as numerical vectors. | | | |
| The most accurate embedding model is Model X. | | | |

The third claim uses a valid source ID, but the source text does not establish which embedding model is most accurate.

This exercise intentionally requires manual judgment. The code checks source IDs, not semantic support.

### Questions

1. Can a valid citation point to irrelevant evidence?
2. Why is ID validation insufficient on its own?
3. What information would be needed to support the third claim?

---

## 12.20 Practical Exercise 5: Handle a Question with No Supporting Source

### Goal

Test whether the citation system avoids inventing references when the available evidence does not answer a question.

### File

`Practical_exercise/citation_missing_source.py`

```python
sources = [
    {
        "source_id": "S1",
        "title": "Embedding Guide",
        "text": "Embeddings represent text as numerical vectors.",
        "url": "https://example.org/embeddings",
    }
]

question = "What is the population of Tokyo?"

# This is a simulated answer for testing the citation logic.
answer = (
    "The supplied source does not contain information "
    "about Tokyo's population."
)

cited_ids = []

source_map = {
    source["source_id"]: source
    for source in sources
}

valid_ids = [
    citation_id
    for citation_id in cited_ids
    if citation_id in source_map
]

print("Question:", question)
print("Answer:", answer)
print("Cited IDs:", cited_ids)
print("Valid cited IDs:", valid_ids)

if not cited_ids:
    print("No citations were supplied.")

if not valid_ids:
    print(
        "No source references were validated. "
        "Do not attach an unrelated source to the answer."
    )
```

### Run the exercise

```bash
python Practical_exercise/citation_missing_source.py
```

### Questions

1. Why does the source not support the answer to the question?
2. Why should the application avoid attaching `[S1]` to an unrelated claim?
3. How should the answer change if a relevant source is retrieved later?
4. Does an empty citation list necessarily mean the application is broken?

This exercise simulates citation handling; it does not call an LLM.

---

## 12.21 Troubleshooting Citation Problems

### Problem 1: A Citation ID Does Not Exist

Possible cause:

The model generated an ID that was not supplied in the source records.

What to check:

- Extract the IDs from the answer.
- Compare them with the supplied source IDs.
- Reject or flag invalid references.

### Problem 2: The Link Is Missing

Possible cause:

The source record did not preserve its URL.

What to check:

- Inspect the source metadata.
- Confirm that the original URL is stored.
- Handle unavailable URLs explicitly.

### Problem 3: The Page Number Is Wrong

Possible cause:

The page number was generated rather than retrieved from trusted source metadata.

What to check:

- Inspect the original document metadata.
- Use the preserved page number.
- Do not accept model-generated page numbers as verified.

### Problem 4: The Citation Exists but Does Not Support the Claim

Possible cause:

The model selected a valid source ID without correctly matching it to the statement.

What to check:

- Read the claim.
- Read the cited passage.
- Determine whether the passage actually supports the claim.
- Flag unsupported claims rather than treating the citation as proof.

### Problem 5: An Answer Contains Unsupported Statements

Possible cause:

The answer includes information absent from the available sources.

What to check:

- Identify the unsupported statement.
- Inspect the supplied evidence.
- Avoid assigning an unrelated citation.
- Ensure the application can communicate uncertainty.

---

## 12.22 Best Practices for Citation Handling

1. Assign unique source IDs to retrieved records.
2. Preserve the original source URL and document metadata.
3. Retain page numbers or section information when available.
4. Give the LLM the source IDs associated with the supplied evidence.
5. Extract citation IDs from the generated answer.
6. Validate each ID against the actual supplied source set.
7. Resolve references using trusted source records.
8. Place citations close to the statements they support.
9. Do not trust model-generated URLs or page numbers without validation.
10. Check whether cited passages support their claims.
11. Avoid citing unrelated sources for unsupported statements.
12. Define behavior for questions with no supporting evidence.
13. Distinguish valid references from correct factual support.
14. Use the most specific reliable source location available.
15. Keep source metadata connected to its associated text throughout the application.

---

## 12.23 Key Takeaways

- A citation connects a generated statement to its supporting source.
- A source is the original resource, while a chunk is a portion of that resource.
- Source IDs provide a convenient way for an LLM to refer to retrieved evidence.
- URLs, titles, page numbers, and other metadata must be preserved if the application needs to display them.
- Generated citation IDs should be validated against the sources actually supplied.
- Valid IDs can be mapped back to trusted source records.
- A valid citation ID does not prove that the source supports the claim.
- Citation generation and citation verification are separate tasks.
- Questions with no supporting evidence should not receive fabricated citations.
- Reliable citation handling helps users verify answers and trace claims to their origins.

**Final lesson:** A citation is not merely a label at the end of a sentence. It must resolve to a real source, and that source must support the claim being made.

---

## Self-Assessment

Answer these questions without looking at the notes.

1. What is a citation in a RAG application?
2. What is the difference between a source, a chunk, and a citation?
3. Why should source IDs be unique?
4. Which metadata should be preserved for citation handling?
5. Why should an application resolve source IDs instead of trusting generated URLs?
6. How can Python extract citation IDs from an answer?
7. What is the difference between citation ID validation and claim-support validation?
8. Why can a valid citation still be incorrect?
9. How should the application handle a question with no supporting source?
10. Why is it important to place citations close to the statements they support?

## Next Step

Complete the five practical exercises and record your observations in the learning repository.

The next lessons can cover hybrid search and reranking, followed by RAG evaluation, as separate topics.
