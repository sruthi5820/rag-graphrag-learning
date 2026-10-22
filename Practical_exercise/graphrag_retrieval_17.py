"""
Lesson 17: GraphRAG Retrieval Strategies

This example demonstrates:
1. Vector-based text retrieval.
2. Entity matching.
3. Graph traversal.
4. Hybrid retrieval.
5. A simple evidence-based answer.

This is a small educational example, not a production GraphRAG system.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# 1. SAMPLE DOCUMENTS
# ---------------------------------------------------------
# Each document contains a unique ID and its text.
# A real application could load these documents from files
# or retrieve them from a document database.

documents = [
    {
        "id": "doc1",
        "text": "Project Alpha uses FastAPI for its backend API.",
    },
    {
        "id": "doc2",
        "text": "FastAPI is a Python web framework used to build APIs.",
    },
    {
        "id": "doc3",
        "text": "Project Alpha uses Chroma for vector storage.",
    },
    {
        "id": "doc4",
        "text": "Chroma stores and searches vector embeddings.",
    },
    {
        "id": "doc5",
        "text": "Project Beta uses Django for its web application.",
    },
]


# ---------------------------------------------------------
# 2. SIMPLE KNOWLEDGE GRAPH
# ---------------------------------------------------------
# Each relationship contains:
# source entity -> relationship -> target entity
#
# This is a plain Python list, not a graph database.

edges = [
    ("Project Alpha", "uses", "FastAPI"),
    ("FastAPI", "is_a", "Python web framework"),
    ("Project Alpha", "uses", "Chroma"),
    ("Chroma", "used_for", "vector storage"),
    ("Project Beta", "uses", "Django"),
]


# ---------------------------------------------------------
# 3. PREPARE THE VECTOR RETRIEVER
# ---------------------------------------------------------
# TF-IDF converts the document texts into numerical vectors.
# Cosine similarity compares the question vector with
# the document vectors.
#
# Unlike a neural embedding model, TF-IDF does not fully
# understand semantic similarity.

document_texts = [
    document["text"]
    for document in documents
]

vectorizer = TfidfVectorizer()

document_vectors = vectorizer.fit_transform(document_texts)


# ---------------------------------------------------------
# 4. VECTOR SEARCH
# ---------------------------------------------------------
def vector_search(question: str, top_k: int = 3) -> list[dict]:
    """
    Retrieve documents with the highest TF-IDF cosine
    similarity to the question.
    """

    # Convert the question into a vector using the same
    # vectorizer that processed the documents.
    question_vector = vectorizer.transform([question])

    # Compare the question vector against all document vectors.
    scores = cosine_similarity(
        question_vector,
        document_vectors,
    )[0]

    # Sort document indexes by similarity, highest first.
    ranked_indexes = scores.argsort()[::-1]

    results = []

    for index in ranked_indexes:
        # Ignore documents with no matching terms.
        if scores[index] <= 0:
            continue

        results.append({
            "id": documents[index]["id"],
            "text": documents[index]["text"],
            "score": float(scores[index]),
        })

        # Stop after retrieving the requested number.
        if len(results) >= top_k:
            break

    return results


# ---------------------------------------------------------
# 5. ENTITY MATCHING
# ---------------------------------------------------------
def match_entities(question: str) -> list[str]:
    """
    Identify known entities mentioned in the question.

    This uses simple string matching.
    A production system may need entity linking or
    named-entity recognition.
    """

    question_lower = question.lower()

    # Extract entity names from graph edges.
    known_entities = set()

    for source, _, target in edges:
        known_entities.add(source)
        known_entities.add(target)

    # Match longer names first to reduce partial matches.
    matched_entities = []

    for entity in sorted(
        known_entities,
        key=len,
        reverse=True,
    ):
        if entity.lower() in question_lower:
            matched_entities.append(entity)

    return matched_entities


# ---------------------------------------------------------
# 6. GRAPH TRAVERSAL
# ---------------------------------------------------------
def graph_traversal(
    starting_entities: list[str],
    max_hops: int = 2,
) -> list[str]:
    """
    Retrieve graph relationships connected to the starting
    entities.

    max_hops limits how far the traversal can explore.

    This example follows relationships in their stored
    direction, from source to target.
    """

    # Keep track of entities already visited.
    visited = set(starting_entities)

    # The first frontier contains the starting entities.
    frontier = set(starting_entities)

    # Store the relationship statements found.
    retrieved_edges = []

    for _ in range(max_hops):
        next_frontier = set()

        for source, relation, target in edges:

            # Follow an outgoing relationship when its source
            # is in the current frontier.
            if source in frontier:
                statement = (
                    f"{source} --{relation}--> {target}"
                )

                if statement not in retrieved_edges:
                    retrieved_edges.append(statement)

                # Continue traversal from the target entity
                # if it has not already been visited.
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)

        # Stop if no additional entities were discovered.
        if not next_frontier:
            break

        frontier = next_frontier

    return retrieved_edges


# ---------------------------------------------------------
# 7. HYBRID RETRIEVAL
# ---------------------------------------------------------
def hybrid_retrieval(
    question: str,
    top_k: int = 3,
    max_hops: int = 2,
) -> dict:
    """
    Combine vector search with entity matching and
    graph traversal.
    """

    # Retrieve relevant text passages.
    vector_results = vector_search(
        question,
        top_k=top_k,
    )

    # Identify entities mentioned in the question.
    entities = match_entities(question)

    # Retrieve relationships connected to those entities.
    graph_results = graph_traversal(
        entities,
        max_hops=max_hops,
    )

    return {
        "question": question,
        "matched_entities": entities,
        "vector_results": vector_results,
        "graph_results": graph_results,
    }


# ---------------------------------------------------------
# 8. SIMPLE EVIDENCE-BASED ANSWER
# ---------------------------------------------------------
def generate_answer(retrieval_result: dict) -> str:
    """
    Create a basic answer from the retrieved evidence.

    This function does not call an LLM. It demonstrates
    how retrieved evidence can be presented with source IDs.
    """

    lines = []

    # Include text evidence with document identifiers.
    for result in retrieval_result["vector_results"]:
        lines.append(
            f"[{result['id']}] {result['text']}"
        )

    # Include relevant graph relationships.
    for relationship in retrieval_result["graph_results"]:
        lines.append(
            f"[Graph evidence] {relationship}"
        )

    if not lines:
        return "No relevant evidence was retrieved."

    return "\n".join(lines)


# ---------------------------------------------------------
# 9. RUN THE EXAMPLE
# ---------------------------------------------------------
if __name__ == "__main__":

    question = (
        "What technologies does Project Alpha use, "
        "and what is FastAPI?"
    )

    # Run vector search separately.
    vector_results = vector_search(question)

    print("\nQUESTION")
    print(question)

    print("\nVECTOR-ONLY RESULTS")

    for result in vector_results:
        print(
            f"[{result['id']}] "
            f"score={result['score']:.3f} "
            f"text={result['text']}"
        )

    # Run the hybrid retrieval pipeline.
    hybrid_results = hybrid_retrieval(question)

    print("\nMATCHED ENTITIES")
    print(hybrid_results["matched_entities"])

    print("\nGRAPH RESULTS")

    for relationship in hybrid_results["graph_results"]:
        print(relationship)

    print("\nHYBRID EVIDENCE")

    answer = generate_answer(hybrid_results)
    print(answer)