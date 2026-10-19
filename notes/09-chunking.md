
# Lesson 9: Chunking Strategies


## 9.1 What Is Chunking?

Chunking is the process of dividing a long piece of text into smaller, manageable sections called **chunks**.

Instead of treating a long document as one large unit, chunking creates smaller units that can be processed independently.

Each chunk should contain a meaningful portion of the original document while preserving as much useful context as possible.

### Example

Original document:

```text
Python is a programming language.
It is widely used for automation and data processing.
Python supports libraries for machine learning.
Machine learning systems can use embeddings to represent text.
Embeddings convert text into numerical vectors.
```

Possible chunks:

**Chunk 1**
```text
Python is a programming language.
It is widely used for automation and data processing.
```

**Chunk 2**
```text
Python supports libraries for machine learning.
Machine learning systems can use embeddings to represent text.
```

**Chunk 3**
```text
Embeddings convert text into numerical vectors.
```

These are illustrative chunks. The ideal boundaries depend on the document's structure and the purpose of the application.

### Why is chunking needed?

- Long documents may exceed model input limits.
- Smaller sections can focus on individual topics.
- A single document may contain many unrelated subjects.
- Meaningful boundaries help preserve context.
- Chunk size and overlap can be adjusted for different content types.

Chunking is not simply splitting text at arbitrary positions. The goal is to create useful, coherent text units.

---

## 9.2 What Makes a Good Chunk?

A good chunk should ideally have the following properties.

### 1. Meaningful content

The chunk should contain enough information to make sense on its own.

Weak chunk:

```text
This method improves
```

Better chunk:

```text
This method improves document processing by reducing
unnecessary whitespace and normalizing line endings.
```

### 2. Appropriate length

A chunk should not be unnecessarily large or too small.

- Very large chunks may contain unrelated information.
- Very small chunks may lose important context.
- Appropriate sizes depend on the document type and application.

### 3. Clear boundaries

Avoid splitting content in the middle of a sentence or important concept when possible.

### 4. Preserved context

A heading, definition, condition, or explanation may be necessary to understand a passage.

### 5. Traceability

A chunk should retain information identifying its source document and its position within that document.

### 6. Minimal unnecessary duplication

Overlapping chunks intentionally repeat some content, but excessive overlap can increase storage and processing costs.

---

## 9.3 Common Chunking Strategies

The main chunking strategies are:

| Strategy | How it works | Main advantage | Main limitation |
|---|---|---|---|
| Fixed-size | Splits text into units of a configured size | Simple and predictable | Can split sentences or concepts |
| Fixed-size with overlap | Repeats part of neighboring chunks | Preserves boundary context | Creates duplicate content |
| Sentence-based | Groups complete sentences | Usually preserves sentence boundaries | Sentence lengths vary |
| Paragraph-based | Uses paragraphs as units | Preserves natural text organization | Paragraph sizes vary |
| Structure-based | Uses headings, sections, pages, or other structure | Preserves document organization | Requires structural information |
| Semantic | Uses changes in meaning to determine boundaries | Can create coherent topic-based chunks | More complex to implement |
| Recursive | Tries larger structural separators before smaller ones | Balances structure and size | Requires careful separator and size rules |

No single strategy is best for every document.

---

## 9.4 Fixed-Size Chunking

Fixed-size chunking divides text into units containing a configured number of words, characters, or tokens.

For example, a word-based implementation might use 100 words per chunk.

### Example

Original text:

```text
Sentence one contains several words.
Sentence two contains several more words.
Sentence three explains another concept.
Sentence four provides additional information.
```

A fixed-size strategy could split the text after a predetermined number of words, regardless of sentence boundaries.

### Python implementation

Create:

`Practical_exercise/chunk_text_01.py`

```python
from pathlib import Path


def chunk_text(
    text: str,
    chunk_size: int = 100,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    words = text.split()

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


if __name__ == "__main__":
    sample_text = (
        "Python is a programming language. "
        "It is used for automation and data processing. "
        "Python also supports machine learning."
    )

    chunks = chunk_text(sample_text, chunk_size=10)

    for index, chunk in enumerate(chunks):
        print(f"\nChunk {index}:")
        print(chunk)
```

### How it works

1. `text.split()` separates text using whitespace.
2. `range()` moves through the word list in increments of `chunk_size`.
3. Each slice selects up to the configured number of words.
4. `" ".join()` combines the selected words into a string.

### Advantages

- Easy to implement.
- Predictable chunk lengths.
- Useful as a baseline for experiments.

### Limitations

- Sentences may be split between chunks.
- Headings may become separated from their content.
- A chunk may contain multiple unrelated topics.

**Important:** This implementation counts words, not model tokens. Word count and token count are different measurements.

---

## 9.5 Fixed-Size Chunking with Overlap

Overlap means repeating a portion of one chunk in the next chunk.

This helps preserve context around chunk boundaries.

### Example

Suppose the chunk size is 10 words and the overlap is 2 words.

Chunk 1:

```text
Python is useful for automation and data processing in businesses.
```

Chunk 2:

```text
in businesses. It can also support machine learning applications.
```

The repeated words are `in businesses.`

The actual result depends on the input text and configured sizes.

### Python implementation

```python
def chunk_text(
    text: str,
    chunk_size: int = 200,
    overlap: int = 30,
) -> list[str]:
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
```

### Understanding the formula

The number of new words introduced by each full chunk is:

```text
step = chunk_size - overlap
```

For example:

```text
chunk_size = 200
overlap = 30
step = 170
```

Each chunk begins 170 words after the previous chunk's starting position. The chunks therefore share 30 words when both chunks are full.

### Advantages

- Helps preserve context across boundaries.
- Reduces the chance that a boundary separates related text.
- Useful for long explanations that continue across sections.

### Limitations

- Repeated text increases the total number of stored words.
- Excessive overlap creates unnecessary duplication.
- Overlap does not automatically fix poor chunk boundaries.

A practical starting experiment is to compare zero overlap with modest overlap values. The best choice depends on the text and downstream task.

---

## 9.6 Sentence-Based Chunking

Sentence-based chunking attempts to keep complete sentences together.

This can produce more readable chunks than splitting text at arbitrary word positions.

### Example

Original text:

```text
Python is easy to learn. It supports many libraries.
Developers use Python for data analysis. It is also used
for machine learning.
```

Possible chunks:

```text
Chunk 1:
Python is easy to learn. It supports many libraries.

Chunk 2:
Developers use Python for data analysis. It is also used
for machine learning.
```

### Simple Python implementation

```python
import re


def chunk_by_sentences(
    text: str,
    max_sentences: int = 3,
) -> list[str]:
    if max_sentences <= 0:
        raise ValueError("max_sentences must be positive")

    text = text.strip()

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    chunks = []

    for i in range(0, len(sentences), max_sentences):
        group = sentences[i:i + max_sentences]
        chunks.append(" ".join(group))

    return chunks
```

### How it works

1. A regular expression looks for whitespace after `.`, `!`, or `?`.
2. The text is divided into sentence-like units.
3. Empty units are removed.
4. Sentences are grouped according to `max_sentences`.

### Advantages

- Keeps many sentences intact.
- Produces readable text.
- Simple to experiment with.

### Limitations

- Abbreviations such as `Dr.` can confuse simple sentence splitting.
- Decimal numbers and unusual punctuation may cause problems.
- Some sentences are much longer than others.
- Languages have different sentence-boundary conventions.

For more reliable sentence detection, a dedicated natural-language-processing sentence tokenizer may be appropriate.

---

## 9.7 Paragraph-Based Chunking

Paragraph-based chunking uses paragraph boundaries to divide text.

It is useful when each paragraph contains a relatively self-contained idea.

### Example

```text
Python is a general-purpose programming language.
It is widely used in software development.

Python has many libraries for data processing.
These libraries help developers analyze structured data.

Python is also used in machine learning.
It supports tools for building and evaluating models.
```

Possible chunks:

**Chunk 1**
```text
Python is a general-purpose programming language.
It is widely used in software development.
```

**Chunk 2**
```text
Python has many libraries for data processing.
These libraries help developers analyze structured data.
```

**Chunk 3**
```text
Python is also used in machine learning.
It supports tools for building and evaluating models.
```

### Python implementation

```python
def chunk_by_paragraphs(text: str) -> list[str]:
    paragraphs = text.split("\n\n")

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]
```

### Advantages

- Preserves natural paragraph boundaries.
- Simple to implement.
- Useful for articles, notes, and reports with good formatting.

### Limitations

- Some paragraphs are too long.
- Some paragraphs contain only a sentence or heading.
- Poorly formatted documents may not contain reliable paragraph breaks.

Paragraph-based chunking can also be combined with size limits, but that requires additional splitting logic.

---

## 9.8 Structure-Based Chunking

Structure-based chunking uses the organization of a document rather than relying only on text length.

Possible boundaries include:

- Headings and subheadings.
- Sections and subsections.
- Pages.
- Chapters.
- HTML elements.
- Markdown headings.
- Tables or code blocks.

### Example

Consider this Markdown document:

```markdown
# Python

Python is a programming language.

## Libraries

Python provides many libraries.

## Applications

Python is used for automation and data processing.
```

A structure-based approach can identify three sections:

```text
Section 1: Python
Content: Python is a programming language.

Section 2: Libraries
Content: Python provides many libraries.

Section 3: Applications
Content: Python is used for automation and data processing.
```

### Simple Markdown section splitter

```python
import re


def split_markdown_sections(text: str) -> list[dict]:
    sections = []
    current_heading = "Introduction"
    current_lines = []

    for line in text.splitlines():
        heading_match = re.match(
            r"^(#{1,6})\s+(.+?)\s*$",
            line,
        )

        if heading_match:
            if current_lines:
                content = "\n".join(current_lines).strip()

                if content:
                    sections.append({
                        "heading": current_heading,
                        "text": content,
                    })

            current_heading = heading_match.group(2)
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        content = "\n".join(current_lines).strip()

        if content:
            sections.append({
                "heading": current_heading,
                "text": content,
            })

    return sections
```

### Limitations of this example

This is a simple learning implementation. It does not preserve heading levels, build a hierarchy of parent and child headings, or specially handle headings inside fenced code blocks.

A more complete Markdown parser should be used when those distinctions matter.

### Advantages

- Preserves document organization.
- Keeps headings associated with their sections.
- Useful for manuals, policies, technical documentation, and reports.

### Limitations

- Requires structural information.
- Sections may have very different lengths.
- Some documents have inconsistent or missing headings.

---

## 9.9 Semantic Chunking

Semantic chunking attempts to split text where the subject or meaning changes.

Instead of using only a fixed word count, it tries to identify groups of sentences that belong together.

### Example

Consider these sentences:

```text
Python is used for automation.
Python supports many data-processing libraries.
The weather forecast predicts heavy rainfall.
The forecast also mentions strong winds.
```

A semantic approach might create two groups:

**Group 1: Python and automation**

```text
Python is used for automation.
Python supports many data-processing libraries.
```

**Group 2: Weather forecast**

```text
The weather forecast predicts heavy rainfall.
The forecast also mentions strong winds.
```

The boundary occurs where the subject changes.

### How semantic chunking can work

A common approach is:

1. Divide the document into sentences.
2. Generate an embedding for each sentence.
3. Compare neighboring sentence embeddings.
4. Identify unusually large changes in similarity.
5. Split at selected boundaries.
6. Check whether the resulting chunks meet size constraints.

### Conceptual example

```text
Sentences
    |
    v
Sentence Embeddings
    |
    v
Compare Neighboring Sentences
    |
    v
Identify Topic Changes
    |
    v
Choose Chunk Boundaries
    |
    v
Validate Chunk Sizes
```

### Advantages

- Can group sentences that discuss the same topic.
- Can separate unrelated subjects within one document.
- May preserve meaning better than arbitrary splitting.

### Limitations

- Requires an embedding model or another semantic analysis method.
- Adds computation and implementation complexity.
- Similarity thresholds need careful selection.
- Similarity changes do not always correspond to ideal boundaries.
- Results must be validated on the intended documents.

Semantic chunking is a technique to explore after understanding simpler strategies. It is not automatically better for every use case.

---

## 9.10 Recursive Chunking

Recursive chunking attempts to split text using larger structural units first and smaller units when necessary.

For example, a splitter may try:

1. Paragraph boundaries.
2. Line boundaries.
3. Sentence boundaries.
4. Word boundaries.
5. Character boundaries.

The exact order depends on the implementation.

### Example

Suppose a document contains three paragraphs, but the first paragraph is very long.

A recursive strategy may:

- Keep short paragraphs intact.
- Split the long paragraph into smaller sections.
- Split an oversized section again if it still exceeds the configured limit.

This helps balance readable boundaries and maximum chunk size.

### Advantages

- Can preserve document structure when possible.
- Can handle mixed paragraph lengths.
- More flexible than a single fixed separator.

### Limitations

- Requires clear splitting rules.
- May still split sentences when necessary.
- Its behavior depends on separator ordering and size measurement.

Recursive splitting is useful when documents have inconsistent structure and strict size constraints.

---

## 9.11 Chunk Size

Chunk size controls the amount of text placed in each chunk.

It can be measured using:

- Words.
- Characters.
- Model tokens.
- Structural units such as sentences or paragraphs.

These measurements are not interchangeable.

### Word count versus token count

Consider:

```text
Document ingestion improves data preparation.
```

The sentence has five whitespace-separated words. A language model's tokenizer may represent it using a different number of tokens.

A token is a unit used by a model's tokenizer. Depending on the tokenizer, a token can represent a word, part of a word, punctuation, or another text unit.

### Small chunks

Potential benefits:

- Focused content.
- Smaller individual text units.
- Less unrelated material inside one chunk.

Potential limitations:

- Important context may be separated.
- Headings or definitions may become detached.
- More individual chunks may be created.

### Large chunks

Potential benefits:

- More surrounding context is retained.
- Related explanations may stay together.
- Fewer chunks may be produced.

Potential limitations:

- A chunk may contain several different subjects.
- More text is processed per chunk.
- Boundaries may be less precise.

### Choosing an initial size

There is no universal ideal chunk size.

For learning, compare sizes such as 100, 200, and 400 words using the same document. Record the number of chunks, their lengths, and whether sentences or ideas are being split.

Treat these values as experimental settings, not production recommendations.

---

## 9.12 Chunk Overlap

Overlap is the amount of content shared between adjacent chunks.

### Example

```text
Chunk size: 8 words
Overlap: 2 words
Step size: 6 words
```

If the word sequence is:

```text
Python is useful for automation and data processing tasks.
```

The first chunk might be:

```text
Python is useful for automation and data processing
```

The next chunk begins at the seventh word, repeating the final two words of the first full chunk where available.

### Calculate overlap percentage

For fixed-size word chunks, the approximate overlap percentage is:

\[
\text{Overlap Percentage}
=
\frac{\text{Overlap}}{\text{Chunk Size}}\times 100
\]

For a chunk size of 200 words and overlap of 30 words:

\[
\frac{30}{200}\times100=15\%
\]

### What happens when overlap increases?

- More context is repeated between chunks.
- The total number of chunks may increase.
- The amount of duplicated text increases.
- Storage and later processing requirements may rise.

### What happens when overlap is zero?

- Each word belongs to only one chunk in a simple non-overlapping splitter.
- There is no intentional repetition between adjacent chunks.
- A concept crossing a boundary may become harder to understand in isolation.

Overlap is a trade-off. More overlap is not always better.

---

## 9.13 Comparing Chunking Strategies

| Strategy | Best suited for | Main concern |
|---|---|---|
| Fixed-size | Simple, consistently sized text units | Can split meaningful boundaries |
| Fixed-size with overlap | Text where adjacent sections need shared context | Repeated content |
| Sentence-based | Prose with meaningful sentence boundaries | Sentence length varies |
| Paragraph-based | Articles and well-formatted text | Paragraph sizes vary |
| Structure-based | Manuals, Markdown, HTML, and reports | Requires reliable structure |
| Semantic | Documents with frequent topic changes | Complexity and tuning |
| Recursive | Documents with mixed formatting and size | More complex splitting rules |

A practical implementation can combine strategies. For example, it might split a Markdown document by headings, then divide sections that exceed a maximum size using sentence boundaries.

---

## 9.14 Preserve Metadata When Creating Chunks

When a document is divided into chunks, its source information should not be lost.

A chunk record can contain:

- `document_id`
- `chunk_index`
- `text`
- `source`
- `heading`, when available

Example:

```python
chunk_record = {
    "document_id": "doc_001",
    "chunk_index": 0,
    "source": "data/sample_documents/example.txt",
    "text": "Document ingestion prepares content.",
}
```

### Why preserve the original document ID?

A single document may produce many chunks.

For example:

```text
Document doc_001
    |
    +-- Chunk 0
    +-- Chunk 1
    +-- Chunk 2
    +-- Chunk 3
```

The shared document ID connects the chunks to their original source. The chunk index identifies the chunk's position within the output.

If the document is reprocessed, chunk indices may change. In applications that require long-term chunk identity, a stable chunk-ID scheme and version tracking may be necessary.

---

## 9.15 Practical Implementation: Word-Based Chunking with Metadata

Create:

`Practical_exercise/chunk_text_02.py`

```python
from pathlib import Path
import json


def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and < chunk_size"
        )

    words = text.split()
    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]

        if chunk_words:
            chunks.append(" ".join(chunk_words))

    return chunks


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_path = (
        project_root
        / "data"
        / "sample_documents"
        / "example.txt"
    )

    output_path = (
        project_root
        / "data"
        / "chunks.json"
    )

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    text = input_path.read_text(
        encoding="utf-8"
    ).strip()

    if not text:
        raise ValueError("Input document is empty")

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap=20,
    )

    chunk_records = [
        {
            "document_id": input_path.name,
            "chunk_index": index,
            "source": str(input_path),
            "text": chunk,
        }
        for index, chunk in enumerate(chunks)
    ]

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            chunk_records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Created {len(chunk_records)} chunks.")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()
```

### Run it

From the project root:

```bash
python Practical_exercise/chunk_text_02.py
```

The resulting file is:

```text
data/chunks.json
```

### Important details

- The script uses word-based chunking.
- It validates chunk size and overlap.
- It preserves the source filename.
- It assigns each chunk an index.
- It writes the result to JSON.

For this learning example, the filename is used as the document ID. A production application should use a suitable stable identifier.

The implementation also permits a final chunk shorter than the configured chunk size. That is normal.

---

## 9.16 Common Chunking Mistakes

### Mistake 1: Choosing chunk size without testing

A chunk size that works for a short article may not work well for a technical manual.

**Better approach:** Compare multiple sizes on representative documents.

### Mistake 2: Using overlap that is too large

Excessive overlap creates duplicated content and increases processing requirements.

**Better approach:** Test a few overlap values rather than assuming the largest is best.

### Mistake 3: Splitting everything by character count

Character-based splitting may divide words and sentences.

**Better approach:** Use word, sentence, paragraph, or structure-based boundaries when appropriate.

### Mistake 4: Ignoring document structure

A heading may become detached from the section it describes.

**Better approach:** Preserve headings or use structure-based splitting when the source format supports it.

### Mistake 5: Assuming all documents have the same structure

A PDF report, a Markdown tutorial, and a short FAQ may need different strategies.

**Better approach:** Select a strategy that matches the document format and content.

### Mistake 6: Forgetting metadata

Once a document is split, the source of a chunk may become unclear.

**Better approach:** Preserve document identity, chunk index, and source information.

### Mistake 7: Confusing words with tokens

A 200-word chunk does not necessarily contain 200 model tokens.

**Better approach:** Use the relevant model tokenizer when actual token limits matter.

### Mistake 8: Ignoring oversized sections

A structure-based splitter may produce a section that is much larger than intended.

**Better approach:** Apply a secondary size-based splitter to oversized sections.

---


## 9.20 Interview Questions and Answers

### Q1. What is chunking?

Chunking divides long text into smaller sections that can be processed independently.

### Q2. Why is chunking necessary?

It helps manage long documents, control text-unit sizes, and preserve meaningful sections for downstream processing.

### Q3. What is fixed-size chunking?

It splits text into units with a configured size measured in words, characters, or tokens.

### Q4. What is chunk overlap?

Overlap is the repeated content shared between adjacent chunks to preserve some context across boundaries.

### Q5. What is the difference between word count and token count?

Word count usually counts whitespace-separated words. Token count depends on a model's tokenizer, which may split a word into multiple tokens or combine text differently.

### Q6. What is sentence-based chunking?

It groups complete sentences into chunks rather than splitting text at arbitrary positions.

### Q7. What is structure-based chunking?

It uses document organization, such as headings, paragraphs, sections, or pages, to determine chunk boundaries.

### Q8. What is semantic chunking?

It attempts to split text when the subject or meaning changes, often using sentence embeddings and similarity measurements.

### Q9. What is recursive chunking?

It tries different separators in order, starting with larger structural boundaries and using smaller boundaries when necessary.

### Q10. What happens when chunk size is too small?

Chunks may lose important context and create excessive fragmentation.

### Q11. What happens when chunk size is too large?

A chunk may contain unrelated topics, making it less focused and increasing the amount of text processed per chunk.

### Q12. Why preserve metadata for each chunk?

Metadata connects a chunk to its original document and helps identify its position and source.

### Q13. Is overlap always beneficial?

No. Overlap may preserve context, but it also increases duplication and storage or processing requirements.

### Q14. Which chunking strategy is best?

There is no universal best strategy. The choice depends on document structure, content, size constraints, and the application's needs.

---

## 9.21 Key Takeaways

1. Chunking divides text into smaller, manageable sections.
2. Fixed-size chunking is simple but can split sentences and concepts.
3. Overlap repeats part of neighboring chunks to preserve context.
4. Sentence-based chunking respects sentence boundaries when detection is accurate.
5. Paragraph-based chunking preserves paragraph organization.
6. Structure-based chunking uses headings and sections.
7. Semantic chunking attempts to identify changes in meaning.
8. Recursive chunking combines different splitting boundaries.
9. Chunk size and overlap should be tested rather than chosen arbitrarily.
10. Word count and token count are different.
11. Document metadata should be preserved when generating chunks.
12. A good chunking strategy balances readability, context, size, and duplication.

**Lesson completion goal:** Implement word-based chunking with configurable size and overlap, compare different configurations, and save chunk records with source metadata to JSON.
