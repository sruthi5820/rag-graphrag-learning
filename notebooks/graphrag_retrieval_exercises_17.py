"""
Lesson 17: GraphRAG Retrieval Strategies
========================================

FULL EXERCISE QUESTIONS

Exercise 1: Direct Fact Lookup
--------------------------------
Question:
"What database does Project Alpha use?"

Tasks:
1. Run vector_search(question).
2. Run hybrid_retrieval(question).
3. Compare the retrieved documents.
4. Check whether graph retrieval adds useful information.
5. Decide which retrieval approach is sufficient.

Exercise 2: Relationship Retrieval
----------------------------------
Question:
"What technologies does Project Alpha use, and what is FastAPI?"

Tasks:
1. Identify the entities in the question.
2. Find graph relationships connected to those entities.
3. Inspect vector search results.
4. Compare vector-only and hybrid evidence.
5. Identify useful relationships that vector retrieval missed.

Exercise 3: Multi-Hop Retrieval
-------------------------------
Question:
"Which programming language is used by the framework used in
Project Alpha?"

Tasks:
1. Identify Project Alpha and other recognized entities.
2. Trace the relevant relationships.
3. Check whether the graph contains enough information.
4. If necessary, add a relationship connecting FastAPI to Python.
5. Run retrieval again.
6. Check whether the evidence supports the answer.

Exercise 4: Compare Retrieval Strategies
----------------------------------------
Prepare questions for these categories:
1. Direct factual lookup.
2. Relationship questions.
3. Multi-hop questions.
4. Broad collection-level questions.

Tasks:
1. Run vector-only and hybrid retrieval.
2. Check whether each result contains the required evidence.
3. Record missing relationships and irrelevant passages.
4. Compare evidence quality and retrieval time.

Exercise 5: Change the Traversal Depth
--------------------------------------
Run graph_traversal(["Project Alpha"], max_hops=1)
and graph_traversal(["Project Alpha"], max_hops=2).

Tasks:
1. Compare the returned relationships.
2. Identify newly retrieved entities.
3. Check whether additional relationships are useful.
4. Explain why excessive traversal can introduce noise and cost.

IMPORTANT:
This is a small educational demonstration.
It uses TF-IDF instead of a neural embedding model.
The graph is stored in a Python list, not a graph database.
The program does not call an LLM.
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

# TfidfVectorizer converts text into numerical vectors.
# cosine_similarity measures how similar two vectors are.
# perf_counter measures how long retrieval takes.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from time import perf_counter


# ============================================================
# 2. SAMPLE DOCUMENTS
# ============================================================

# These documents act as our small knowledge base.
#
# Each document has:
# - id: a unique identifier used for source tracking.
# - text: the actual information stored in the document.
#
# In a real RAG application, documents could come from PDFs,
# websites, Markdown files, databases, or other sources.

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
    {
        "id": "doc6",
        "text": "Django is a Python web framework.",
    },
    {
        "id": "doc7",
        "text": (
            "Common retrieval challenges include irrelevant results, "
            "missing evidence, slow searches, and unsupported answers."
        ),
    },
    {
        "id": "doc8",
        "text": (
            "Hybrid retrieval combines keyword or vector search "
            "with additional evidence from connected relationships."
        ),
    },
]


# ============================================================
# 3. KNOWLEDGE GRAPH
# ============================================================

# A graph contains entities and relationships.
#
# Each tuple follows this format:
# (source_entity, relationship, target_entity)
#
# Example:
# ("Project Alpha", "uses", "FastAPI")
#
# This means:
# Project Alpha --uses--> FastAPI
#
# We use a Python list for simplicity.
# A production system might use a graph database.

edges = [
    ("Project Alpha", "uses", "FastAPI"),
    ("FastAPI", "is_a", "Python web framework"),
    ("FastAPI", "written_in", "Python"),
    ("Project Alpha", "uses", "Chroma"),
    ("Chroma", "used_for", "vector storage"),
    ("Project Beta", "uses", "Django"),
    ("Django", "is_a", "Python web framework"),
    ("Django", "written_in", "Python"),
]


# ============================================================
# 4. PREPARE THE VECTOR SEARCH INDEX
# ============================================================

# TF-IDF assigns numerical weights to words in documents.
#
# The vectorizer learns its vocabulary from the documents.
# It then converts each document into a numerical vector.
#
# We create the vectors once instead of rebuilding them
# every time a question is asked.

document_texts = [
    document["text"]
    for document in documents
]

vectorizer = TfidfVectorizer()

document_vectors = vectorizer.fit_transform(document_texts)


# ============================================================
# 5. VECTOR SEARCH
# ============================================================

def vector_search(question: str, top_k: int = 3) -> list[dict]:
    """
    Retrieve documents that match the question using TF-IDF.

    Simple explanation:
    1. Convert the question into a numerical vector.
    2. Compare it with each document vector.
    3. Rank documents by cosine similarity.
    4. Return the top matching documents.

    A higher similarity score means the document has a
    stronger word-based match with the question.

    Note:
    TF-IDF is not the same as a modern semantic embedding model.
    It may miss relevant text when different words express
    similar meanings.
    """

    # Convert the question into a vector using the vocabulary
    # learned from our existing documents.
    question_vector = vectorizer.transform([question])

    # Calculate similarity between the question and all documents.
    scores = cosine_similarity(
        question_vector,
        document_vectors,
    )[0]

    # Sort document positions from highest similarity to lowest.
    ranked_indexes = scores.argsort()[::-1]

    results = []

    for index in ranked_indexes:

        # A score of zero means there were no shared weighted
        # vocabulary terms. Skip these documents.
        if scores[index] <= 0:
            continue

        results.append({
            "id": documents[index]["id"],
            "text": documents[index]["text"],
            "score": float(scores[index]),
        })

        # Stop when we have enough results.
        if len(results) >= top_k:
            break

    return results


# ============================================================
# 6. ENTITY MATCHING
# ============================================================

def match_entities(question: str) -> list[str]:
    """
    Find known graph entities mentioned in a question.

    Simple explanation:
    1. Collect entity names from the graph.
    2. Look for those names in the question.
    3. Return the matching entities.

    This is basic string matching. It does not understand
    synonyms or automatically recognize unknown entities.
    """

    question_lower = question.lower()

    # Every source and target in an edge is a graph entity.
    known_entities = set()

    for source, _, target in edges:
        known_entities.add(source)
        known_entities.add(target)

    matched_entities = []

    # Check longer names first to reduce partial-name matches.
    for entity in sorted(
        known_entities,
        key=len,
        reverse=True,
    ):
        if entity.lower() in question_lower:
            matched_entities.append(entity)

    return matched_entities


# ============================================================
# 7. GRAPH TRAVERSAL
# ============================================================

def graph_traversal(
    starting_entities: list[str],
    max_hops: int = 2,
) -> list[str]:
    """
    Follow graph relationships from the starting entities.

    What is a hop?
    One hop means following one relationship.

    Example:
    Project Alpha --uses--> FastAPI

    This is one hop.

    Project Alpha --uses--> FastAPI --written_in--> Python

    This path has two hops.

    The function follows relationships in their stored direction.
    """

    if max_hops < 0:
        raise ValueError("max_hops must be zero or greater")

    # Entities already discovered.
    visited = set(starting_entities)

    # Entities that we will explore during the current hop.
    frontier = set(starting_entities)

    # Store the relationship statements we retrieve.
    retrieved_edges = []

    # Repeat the traversal up to max_hops times.
    for _ in range(max_hops):

        next_frontier = set()

        # Examine every relationship in the graph.
        for source, relation, target in edges:

            # Follow a relationship if its source is in
            # the current group of entities being explored.
            if source in frontier:

                statement = (
                    f"{source} --{relation}--> {target}"
                )

                if statement not in retrieved_edges:
                    retrieved_edges.append(statement)

                # Add newly discovered entities to the next
                # group so their relationships can be explored.
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)

        # Stop early if no new entities were found.
        if not next_frontier:
            break

        frontier = next_frontier

    return retrieved_edges


# ============================================================
# 8. HYBRID RETRIEVAL
# ============================================================

def hybrid_retrieval(
    question: str,
    top_k: int = 3,
    max_hops: int = 2,
) -> dict:
    """
    Combine vector search with graph retrieval.

    Simple explanation:
    1. Vector search finds relevant text passages.
    2. Entity matching finds known entities in the question.
    3. Graph traversal retrieves connected relationships.
    4. The function returns both kinds of evidence.

    This example combines the results but does not implement
    a separate ranking model for graph relationships.
    """

    # Part A: retrieve matching text passages.
    vector_results = vector_search(
        question,
        top_k=top_k,
    )

    # Part B: find entities named in the question.
    entities = match_entities(question)

    # Part C: follow relationships from those entities.
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


# ============================================================
# 9. DISPLAY VECTOR RESULTS
# ============================================================

def display_vector_results(results: list[dict]) -> None:
    """
    Print vector search results in a readable format.
    """

    if not results:
        print("No matching documents found.")
        return

    for result in results:
        print(
            f"[{result['id']}] "
            f"score={result['score']:.3f}\n"
            f"  {result['text']}"
        )


# ============================================================
# 10. DISPLAY HYBRID RESULTS
# ============================================================

def display_hybrid_results(result: dict) -> None:
    """
    Display the entities, text passages, and relationships
    retrieved by the hybrid approach.
    """

    print("\nMatched entities:")
    print(result["matched_entities"])

    print("\nVector evidence:")
    display_vector_results(result["vector_results"])

    print("\nGraph evidence:")

    if result["graph_results"]:
        for relationship in result["graph_results"]:
            print(f"- {relationship}")
    else:
        print("No connected relationships found.")


# ============================================================
# 11. EXERCISE 1: DIRECT FACT LOOKUP
# ============================================================

def exercise_1() -> None:
    """
    Question:
    "What database does Project Alpha use?"

    Compare vector-only and hybrid retrieval.

    Note:
    Our sample data says Project Alpha uses Chroma for vector
    storage. The question uses the word 'database', so TF-IDF
    may not retrieve the best evidence because the exact word
    'database' is absent from the relevant document.
    """

    print("\n" + "=" * 70)
    print("EXERCISE 1: DIRECT FACT LOOKUP")
    print("=" * 70)

    question = "What database does Project Alpha use?"

    print(f"\nQuestion: {question}")

    # Measure how long vector-only retrieval takes.
    start = perf_counter()
    vector_results = vector_search(question)
    vector_time = perf_counter() - start

    print("\n--- Vector-only retrieval ---")
    display_vector_results(vector_results)
    print(f"Vector retrieval time: {vector_time:.6f} seconds")

    # Measure how long hybrid retrieval takes.
    start = perf_counter()
    hybrid_results = hybrid_retrieval(question)
    hybrid_time = perf_counter() - start

    print("\n--- Hybrid retrieval ---")
    display_hybrid_results(hybrid_results)
    print(f"Hybrid retrieval time: {hybrid_time:.6f} seconds")

    print("\nWhat to observe:")
    print("- Did vector search retrieve the Chroma document?")
    print("- Did graph traversal retrieve Project Alpha's connections?")
    print("- Was the extra graph evidence useful?")


# ============================================================
# 12. EXERCISE 2: RELATIONSHIP RETRIEVAL
# ============================================================

def exercise_2() -> None:
    """
    Question:
    "What technologies does Project Alpha use, and what is FastAPI?"

    Find the entities and their connected relationships.
    Compare vector-only and hybrid evidence.
    """

    print("\n" + "=" * 70)
    print("EXERCISE 2: RELATIONSHIP RETRIEVAL")
    print("=" * 70)

    question = (
        "What technologies does Project Alpha use, "
        "and what is FastAPI?"
    )

    print(f"\nQuestion: {question}")

    print("\n--- Vector-only retrieval ---")
    display_vector_results(vector_search(question))

    print("\n--- Hybrid retrieval ---")
    result = hybrid_retrieval(question)
    display_hybrid_results(result)

    print("\nWhat to observe:")
    print("- Which entities were matched?")
    print("- Did the graph retrieve the FastAPI relationship?")
    print("- Which useful facts came from the text documents?")
    print("- Did graph retrieval add evidence missing from vector search?")


# ============================================================
# 13. EXERCISE 3: MULTI-HOP RETRIEVAL
# ============================================================

def exercise_3() -> None:
    """
    Question:
    "Which programming language is used by the framework used in
    Project Alpha?"

    This requires connecting:
    Project Alpha -> FastAPI -> Python.

    The graph already contains the relationship:
    FastAPI --written_in--> Python

    Therefore, no additional edge is needed in this example.
    """

    print("\n" + "=" * 70)
    print("EXERCISE 3: MULTI-HOP RETRIEVAL")
    print("=" * 70)

    question = (
        "Which programming language is used by the "
        "framework used in Project Alpha?"
    )

    print(f"\nQuestion: {question}")

    # First inspect the entities recognized in the question.
    entities = match_entities(question)

    print("\nMatched entities:")
    print(entities)

    # Retrieve relationships up to two hops away.
    graph_results = graph_traversal(
        ["Project Alpha"],
        max_hops=2,
    )

    print("\nRelationships found from Project Alpha:")

    for relationship in graph_results:
        print(f"- {relationship}")

    print("\n--- Vector-only evidence ---")
    display_vector_results(vector_search(question))

    print("\n--- Hybrid evidence ---")
    hybrid_results = hybrid_retrieval(question)
    display_hybrid_results(hybrid_results)

    print("\nWhat to observe:")
    print("- Can you trace Project Alpha to FastAPI and then Python?")
    print("- Does the retrieved evidence support Python as the answer?")
    print("- What happens if the FastAPI-to-Python edge is removed?")


# ============================================================
# 14. EXERCISE 4: COMPARE RETRIEVAL STRATEGIES
# ============================================================

def exercise_4() -> None:
    """
    Compare vector-only and hybrid retrieval across four question
    categories.

    These examples are test questions, not a formal benchmark.
    The broad question is difficult for this small dataset because
    only a few sample documents are available.
    """

    print("\n" + "=" * 70)
    print("EXERCISE 4: COMPARE RETRIEVAL STRATEGIES")
    print("=" * 70)

    test_questions = {
        "Direct factual lookup": [
            "What database does Project Alpha use?",
            "Which framework does Project Beta use?",
            "What does Chroma store?",
        ],
        "Relationship question": [
            "What technologies does Project Alpha use?",
            "What is FastAPI?",
            "What is Django?",
        ],
        "Multi-hop question": [
            "Which programming language is used by the framework in Project Alpha?",
            "What is the purpose of the technology used for vector storage?",
            "Which framework used by a project is a Python web framework?",
        ],
        "Broad collection-level question": [
            "What technical challenges are mentioned in these documents?",
            "What retrieval approaches are described?",
            "What common themes appear in the sample documents?",
        ],
    }

    # Store the results so they can be compared after all
    # questions have been processed.
    comparison_rows = []

    for category, questions in test_questions.items():

        print(f"\n\n### Category: {category}")

        for question in questions:

            print(f"\nQuestion: {question}")

            # Measure vector-only retrieval time.
            start = perf_counter()
            vector_results = vector_search(question)
            vector_time = perf_counter() - start

            # Measure hybrid retrieval time.
            start = perf_counter()
            hybrid_results = hybrid_retrieval(question)
            hybrid_time = perf_counter() - start

            print("\nVector-only document IDs:")
            print([item["id"] for item in vector_results])

            print("\nHybrid document IDs:")
            print([
                item["id"]
                for item in hybrid_results["vector_results"]
            ])

            print("\nHybrid graph evidence:")
            if hybrid_results["graph_results"]:
                for relationship in hybrid_results["graph_results"]:
                    print(f"- {relationship}")
            else:
                print("No graph relationships retrieved.")

            print(
                f"\nVector time: {vector_time:.6f} seconds"
            )
            print(
                f"Hybrid time: {hybrid_time:.6f} seconds"
            )

            comparison_rows.append({
                "category": category,
                "question": question,
                "vector_time": vector_time,
                "hybrid_time": hybrid_time,
                "vector_count": len(vector_results),
                "hybrid_graph_count": len(
                    hybrid_results["graph_results"]
                ),
            })

    print("\n\n--- COMPARISON SUMMARY ---")

    print(
        f"{'Category':32} "
        f"{'Vector docs':12} "
        f"{'Graph edges':12} "
        f"{'Vector sec':12} "
        f"{'Hybrid sec':12}"
    )

    print("-" * 85)

    for row in comparison_rows:
        print(
            f"{row['category'][:31]:32} "
            f"{row['vector_count']:<12} "
            f"{row['hybrid_graph_count']:<12} "
            f"{row['vector_time']:<12.6f} "
            f"{row['hybrid_time']:<12.6f}"
        )

    print("\nWhat to observe:")
    print("- Does hybrid retrieval add useful relationships?")
    print("- Are the retrieved passages actually relevant?")
    print("- Which question types need evidence from multiple sources?")
    print("- Is the extra retrieval time justified?")

    print(
        "\nImportant: retrieval time depends on the computer, "
        "dataset size, and execution environment. These small "
        "timings are educational observations, not benchmarks."
    )


# ============================================================
# 15. EXERCISE 5: CHANGE TRAVERSAL DEPTH
# ============================================================

def exercise_5() -> None:
    """
    Compare graph traversal using one hop and two hops.

    One hop:
    Project Alpha -> FastAPI
    Project Alpha -> Chroma

    Two hops can also explore relationships from FastAPI
    and Chroma, such as FastAPI -> Python and Chroma -> vector storage.
    """

    print("\n" + "=" * 70)
    print("EXERCISE 5: CHANGE TRAVERSAL DEPTH")
    print("=" * 70)

    starting_entities = ["Project Alpha"]

    # Run graph traversal with one hop.
    one_hop_results = graph_traversal(
        starting_entities,
        max_hops=1,
    )

    print("\n--- Results with max_hops=1 ---")

    for relationship in one_hop_results:
        print(f"- {relationship}")

    # Run graph traversal with two hops.
    two_hop_results = graph_traversal(
        starting_entities,
        max_hops=2,
    )

    print("\n--- Results with max_hops=2 ---")

    for relationship in two_hop_results:
        print(f"- {relationship}")

    # Find the relationships that appear only with two hops.
    new_relationships = [
        relationship
        for relationship in two_hop_results
        if relationship not in one_hop_results
    ]

    print("\n--- Additional relationships at two hops ---")

    if new_relationships:
        for relationship in new_relationships:
            print(f"- {relationship}")
    else:
        print("No additional relationships were found.")

    print("\nWhat to observe:")
    print("- How many more relationships were found at two hops?")
    print("- Are the new relationships relevant to the question?")
    print("- Could even deeper traversal introduce unrelated evidence?")


# ============================================================
# 16. RUN ALL FIVE EXERCISES
# ============================================================

if __name__ == "__main__":

    # Each function implements one exercise.
    # Running this file executes all five exercises in order.

    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()

    