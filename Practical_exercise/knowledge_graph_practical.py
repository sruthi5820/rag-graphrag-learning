"""
KNOWLEDGE GRAPH PRACTICAL EXERCISE

In this program, we will learn how to:
1. Create entities (nodes) and add properties to them.
2. Connect entities using relationships (edges).
3. Store the source document and evidence for each relationship.
4. Find incoming and outgoing connections.
5. Find paths between entities.
6. Validate relationships and graph structure.
7. Save and reload the graph using JSON.
8. Visualize a complete graph and a smaller graph.

A knowledge graph stores information as connected entities.

Example:
Alice --WORKS_AT--> SDI

Alice and SDI are entities.
WORKS_AT is the relationship between them.
"""


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import json
# json helps us save Python data into a JSON file and read it back.

from pathlib import Path
# Path helps us create and manage file and folder paths.

import matplotlib.pyplot as plt
# Matplotlib is used to display and save graph pictures.

import networkx as nx
# NetworkX helps us create, connect, search, and analyze graph data.


# ============================================================
# 2. PROJECT SETUP
# ============================================================

# Create a folder where the output files will be saved.
# If the folder does not exist, Python creates it.
OUTPUT_DIR = Path("data/graph_examples")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create an empty directed graph.
# A directed graph has relationships with a direction.
# Example: Alice -> SDI does not automatically mean SDI -> Alice.
graph = nx.DiGraph()


# ============================================================
# 3. CREATE ENTITIES WITH PROPERTIES
# ============================================================

# Entities are the things we want to represent in our graph.
# Examples: people, organizations, technologies, and documents.
#
# Each entity has properties that describe it.
# For example, Alice is a Person who belongs to the Research department.

entities = {
    "Alice": {
        "entity_type": "Person",
        "department": "Research",
    },
    "Bob": {
        "entity_type": "Person",
        "department": "Engineering",
    },
    "SDI": {
        "entity_type": "Organization",
    },
    "Artificial Intelligence": {
        "entity_type": "TechnicalConcept",
    },
    "Machine Learning": {
        "entity_type": "TechnicalConcept",
    },
    "RAG": {
        "entity_type": "TechnicalConcept",
    },
    "GraphRAG": {
        "entity_type": "TechnicalConcept",
    },
    "Vector Database": {
        "entity_type": "Technology",
    },
    "Embeddings": {
        "entity_type": "TechnicalConcept",
    },
    "Semantic Search": {
        "entity_type": "Technology",
    },
    "Language Model": {
        "entity_type": "Technology",
    },
    "Document": {
        "entity_type": "DocumentType",
    },
    "Research Project": {
        "entity_type": "Project",
    },
    "Question Answering": {
        "entity_type": "Application",
    },
    "Knowledge Graph": {
        "entity_type": "TechnicalConcept",
    },
    "Unconnected Example": {
        "entity_type": "TestEntity",
    },
}

# Add every entity to the graph.
# The entity name becomes the node ID.
# The dictionary values become properties stored on that node.
for entity_name, properties in entities.items():
    graph.add_node(entity_name, **properties)

# Example:
# graph.nodes["Alice"] contains:
# {
#     "entity_type": "Person",
#     "department": "Research"
# }


# ============================================================
# 4. CREATE RELATIONSHIPS WITH EVIDENCE AND SOURCE IDS
# ============================================================

# Relationships explain how two entities are connected.
#
# Each relationship contains five values:
# 1. source       = the starting entity
# 2. target       = the ending entity
# 3. relation     = how the entities are connected
# 4. document_id  = the document where we found the information
# 5. evidence     = the sentence supporting the relationship
#
# Example:
# Alice --WORKS_AT--> SDI
#
# doc_001 contains the supporting sentence:
# "Alice works at SDI."

relationships = [
    (
        "Alice",
        "SDI",
        "WORKS_AT",
        "doc_001",
        "Alice works at SDI.",
    ),
    (
        "Bob",
        "SDI",
        "WORKS_AT",
        "doc_002",
        "Bob works at SDI.",
    ),
    (
        "Alice",
        "Artificial Intelligence",
        "STUDIES",
        "doc_003",
        "Alice studies Artificial Intelligence.",
    ),
    (
        "Bob",
        "Machine Learning",
        "STUDIES",
        "doc_004",
        "Bob studies Machine Learning.",
    ),
    (
        "Machine Learning",
        "Artificial Intelligence",
        "RELATED_TO",
        "doc_005",
        "Machine Learning is related to Artificial Intelligence.",
    ),
    (
        "Artificial Intelligence",
        "RAG",
        "INCLUDES",
        "doc_006",
        "RAG is a topic associated with Artificial Intelligence.",
    ),
    (
        "Artificial Intelligence",
        "GraphRAG",
        "INCLUDES",
        "doc_007",
        "GraphRAG is associated with Artificial Intelligence.",
    ),
    (
        "GraphRAG",
        "RAG",
        "EXTENDS",
        "doc_008",
        "GraphRAG extends the RAG approach with graph-based information.",
    ),
    (
        "RAG",
        "Embeddings",
        "USES",
        "doc_009",
        "The example RAG system uses embeddings.",
    ),
    (
        "RAG",
        "Vector Database",
        "USES",
        "doc_010",
        "The example RAG system uses a vector database.",
    ),
    (
        "Semantic Search",
        "Embeddings",
        "USES",
        "doc_011",
        "Semantic search can use embeddings.",
    ),
    (
        "GraphRAG",
        "Vector Database",
        "USES",
        "doc_012",
        "The example GraphRAG system uses a vector database.",
    ),
    (
        "GraphRAG",
        "Knowledge Graph",
        "USES",
        "doc_013",
        "The example GraphRAG system uses a knowledge graph.",
    ),
    (
        "Language Model",
        "Question Answering",
        "USED_IN",
        "doc_014",
        "A language model can be used in a question-answering application.",
    ),
    (
        "RAG",
        "Question Answering",
        "USED_IN",
        "doc_015",
        "RAG can provide supporting context for question answering.",
    ),
    (
        "GraphRAG",
        "Question Answering",
        "USED_IN",
        "doc_016",
        "GraphRAG can support question-answering applications.",
    ),
    (
        "Alice",
        "Research Project",
        "WORKS_ON",
        "doc_017",
        "Alice works on the research project.",
    ),
    (
        "Bob",
        "Research Project",
        "WORKS_ON",
        "doc_018",
        "Bob works on the research project.",
    ),
    (
        "Research Project",
        "GraphRAG",
        "STUDIES",
        "doc_019",
        "The research project studies GraphRAG.",
    ),
    (
        "Document",
        "RAG",
        "DESCRIBES",
        "doc_020",
        "A document describes RAG.",
    ),
    (
        "Document",
        "Knowledge Graph",
        "MENTIONS",
        "doc_021",
        "A document mentions knowledge graphs.",
    ),
    (
        "Alice",
        "Document",
        "AUTHORED",
        "doc_022",
        "Alice authored the example document.",
    ),
    (
        "Knowledge Graph",
        "GraphRAG",
        "RELATED_TO",
        "doc_023",
        "Knowledge graphs are related to GraphRAG.",
    ),
]

# Add every relationship to the graph.
# NetworkX creates the edge from source to target.
# The remaining values are stored as properties of the edge.
for source, target, relation, document_id, evidence in relationships:
    graph.add_edge(
        source,
        target,
        relation=relation,
        source_document_id=document_id,
        evidence=evidence,
    )

# Why store evidence?
# If a user asks why Alice is connected to SDI, we can show
# the sentence and document that support the relationship.


# ============================================================
# 5. DISPLAY GRAPH STATISTICS AND TRIPLES
# ============================================================

print("\n" + "=" * 65)
print("1. KNOWLEDGE GRAPH STATISTICS")
print("=" * 65)

# A node represents an entity.
print("Number of nodes:", graph.number_of_nodes())

# An edge represents a relationship between two entities.
print("Number of edges:", graph.number_of_edges())

print("\nALL GRAPH TRIPLES")

# A triple is written as:
# (subject, relationship, object)
#
# Example:
# (Alice, WORKS_AT, SDI)
#
# This format is useful for representing knowledge in a simple way.
for source, target, attributes in graph.edges(data=True):
    print(
        f"({source}, {attributes['relation']}, {target})"
    )


# ============================================================
# 6. FIND INCOMING AND OUTGOING NEIGHBORS
# ============================================================

def show_neighbors(graph, entity):
    """Print the entities connected to the given entity."""

    # Check whether the entity exists in the graph.
    # This prevents errors when an unknown name is provided.
    if entity not in graph:
        print(f"Entity not found: {entity}")
        return

    # Outgoing neighbors are entities that this entity points to.
    # Example: RAG -> Embeddings.
    outgoing = list(graph.successors(entity))

    # Incoming neighbors are entities that point to this entity.
    # Example: GraphRAG -> RAG means GraphRAG is an incoming neighbor of RAG.
    incoming = list(graph.predecessors(entity))

    print(f"\nEntity: {entity}")
    print("Outgoing neighbors:", outgoing)
    print("Incoming neighbors:", incoming)


print("\n" + "=" * 65)
print("2. GRAPH NEIGHBORS")
print("=" * 65)

# Find entities that point from or to RAG.
show_neighbors(graph, "RAG")

# Check which entities connect to Artificial Intelligence.
show_neighbors(graph, "Artificial Intelligence")

# Check Alice's connections.
show_neighbors(graph, "Alice")


# ============================================================
# 7. FIND PATHS BETWEEN ENTITIES
# ============================================================

def show_path(graph, source, target):
    """Find and display the shortest directed path."""

    print(f"\nPath: {source} -> {target}")

    # First, check that the starting entity exists.
    if source not in graph:
        print(f"Source entity does not exist: {source}")
        return

    # Then, check that the destination entity exists.
    if target not in graph:
        print(f"Target entity does not exist: {target}")
        return

    try:
        # Find a path that follows the direction of each edge.
        # shortest_path returns the path with the fewest edges.
        path = nx.shortest_path(
            graph,
            source=source,
            target=target,
        )

        # Print the entity names in the path.
        print("Nodes:", " -> ".join(path))

        print("Relationships:")

        # Read each pair of connected entities in the path.
        for current, next_node in zip(path, path[1:]):
            attributes = graph[current][next_node]

            # Print the relationship between the two entities.
            print(
                f"  {current} "
                f"--{attributes['relation']}--> "
                f"{next_node}"
            )

    except nx.NetworkXNoPath:
        # Both entities exist, but no directed route connects them.
        print("No directed path exists between these entities.")


print("\n" + "=" * 65)
print("3. PATH FINDING")
print("=" * 65)

# Find a path from Alice to Question Answering.
show_path(graph, "Alice", "Question Answering")

# Find a path from Bob to GraphRAG.
show_path(graph, "Bob", "GraphRAG")

# Both entities exist, but this starting entity has no outgoing edges.
# Therefore, a directed path from it to RAG should not exist.
show_path(graph, "Unconnected Example", "RAG")


# ============================================================
# 8. ADD AND INSPECT NODE PROPERTIES
# ============================================================

print("\n" + "=" * 65)
print("4. NODE PROPERTIES")
print("=" * 65)

# Update Alice's department and entity type.
# These values are already present, but this shows how to update them.
graph.nodes["Alice"]["department"] = "Research"
graph.nodes["Alice"]["entity_type"] = "Person"

# Add a new property to the SDI node.
graph.nodes["SDI"]["organization_type"] = "ExampleOrganization"

# Print the properties of specific entities.
print("Alice:", dict(graph.nodes["Alice"]))
print("SDI:", dict(graph.nodes["SDI"]))

print("\nAll nodes and their properties:")

# data=True returns each node along with its property dictionary.
for node, attributes in graph.nodes(data=True):
    print(node, dict(attributes))


# ============================================================
# 9. INSPECT EDGE EVIDENCE AND SOURCE DOCUMENTS
# ============================================================

print("\n" + "=" * 65)
print("5. EDGE EVIDENCE AND SOURCE DOCUMENTS")
print("=" * 65)

# Choose a few relationships to inspect.
edges_to_inspect = [
    ("Alice", "SDI"),
    ("Alice", "Research Project"),
    ("GraphRAG", "Question Answering"),
]

for source, target in edges_to_inspect:

    # Check that the relationship exists before reading its properties.
    if graph.has_edge(source, target):
        print(f"\n{source} -> {target}")

        # Print the relationship type, source document ID, and evidence.
        print(dict(graph[source][target]))

# Example of updating the evidence stored on an existing relationship.
graph["Alice"]["SDI"]["evidence"] = "Alice works at SDI."

# Important:
# Source document IDs and evidence help trace where graph facts came from.
# In a real RAG system, these should refer to actual source documents
# and accurate supporting text.


# ============================================================
# 10. VALIDATE RELATIONSHIP TYPES
# ============================================================

def has_relationship(
    graph,
    source,
    target,
    expected_relation,
):
    """Check whether two entities have the expected relationship."""

    # If the edge does not exist, the expected relationship is false.
    if not graph.has_edge(source, target):
        return False

    # If the edge exists, compare its stored relationship type
    # with the relationship type we expected.
    return (
        graph[source][target].get("relation")
        == expected_relation
    )


print("\n" + "=" * 65)
print("6. RELATIONSHIP VALIDATION")
print("=" * 65)

# Test three possible relationships.
tests = [
    ("Alice", "SDI", "WORKS_AT"),
    ("Alice", "SDI", "STUDIES"),
    ("Alice", "GraphRAG", "WORKS_AT"),
]

for source, target, relation in tests:
    result = has_relationship(
        graph,
        source,
        target,
        relation,
    )

    print(
        f"{source} --{relation}--> {target}: {result}"
    )

# Expected results:
# Alice --WORKS_AT--> SDI: True
# Alice --STUDIES--> SDI: False
# Alice --WORKS_AT--> GraphRAG: False


# ============================================================
# 11. VALIDATE THE GRAPH STRUCTURE
# ============================================================

print("\n" + "=" * 65)
print("7. STRUCTURAL VALIDATION")
print("=" * 65)

# Make sure the graph contains enough nodes and edges for this exercise.
assert graph.number_of_nodes() >= 10
assert graph.number_of_edges() >= 15

# Confirm that important entities and relationships exist.
assert "Alice" in graph
assert "GraphRAG" in graph
assert graph.has_edge("Alice", "SDI")

# Confirm that the relationship type is correct.
assert has_relationship(
    graph,
    "Alice",
    "SDI",
    "WORKS_AT",
)

# Every entity must have an entity_type property.
# If a property is missing, assert stops the program with an error.
for node, attributes in graph.nodes(data=True):
    assert attributes.get("entity_type"), (
        f"Missing entity_type for node: {node}"
    )

# Every relationship must have a type, source document ID,
# and supporting evidence.
for source, target, attributes in graph.edges(data=True):
    assert attributes.get("relation"), (
        f"Missing relation: {source} -> {target}"
    )

    assert attributes.get("source_document_id"), (
        f"Missing source document ID: {source} -> {target}"
    )

    assert attributes.get("evidence"), (
        f"Missing evidence: {source} -> {target}"
    )

# Confirm that Alice can reach GraphRAG by following directed edges.
assert nx.has_path(graph, "Alice", "GraphRAG")

# Confirm that the unconnected test entity cannot reach RAG.
assert not nx.has_path(
    graph,
    "Unconnected Example",
    "RAG",
)

print("All structural validation checks passed.")

# Remember:
# assert is useful for checking assumptions automatically.
# If an assertion fails, check the graph data to find the problem.


# ============================================================
# 12. EXPORT THE GRAPH TO JSON
# ============================================================

print("\n" + "=" * 65)
print("8. EXPORT GRAPH DATA")
print("=" * 65)

# Convert the graph into ordinary Python dictionaries and lists.
# JSON can store these types of data.
#
# Each node contains its ID and properties.
# Each edge contains its source, target, and properties.

graph_data = {
    "nodes": [
        {
            "id": node,
            **attributes,
        }
        for node, attributes in graph.nodes(data=True)
    ],
    "edges": [
        {
            "source": source,
            "target": target,
            **attributes,
        }
        for source, target, attributes in graph.edges(data=True)
    ],
}

# Create the full path for the JSON output file.
json_path = OUTPUT_DIR / "knowledge_graph.json"

# Open the file in write mode and save the graph as formatted JSON.
with json_path.open("w", encoding="utf-8") as file:
    json.dump(
        graph_data,
        file,
        indent=2,
        ensure_ascii=False,
    )

print("JSON file saved to:", json_path)

# Why JSON?
# JSON lets us store graph information outside Python.
# We can load the information again later without recreating
# all the entities and relationships manually.


# ============================================================
# 13. RELOAD THE GRAPH FROM JSON
# ============================================================

print("\n" + "=" * 65)
print("9. RELOAD AND VERIFY JSON DATA")
print("=" * 65)

# Open the JSON file and convert its contents back into Python data.
with json_path.open("r", encoding="utf-8") as file:
    loaded_data = json.load(file)

# Create a new, empty graph to prove that we can rebuild it.
reloaded_graph = nx.DiGraph()

# Restore all nodes and their properties.
for node_data in loaded_data["nodes"]:

    # Make a copy so that removing the ID does not change loaded_data.
    node_data = node_data.copy()

    # Separate the node ID from the other properties.
    node_id = node_data.pop("id")

    # Add the node to the new graph with its properties.
    reloaded_graph.add_node(
        node_id,
        **node_data,
    )

# Restore all relationships and their properties.
for edge_data in loaded_data["edges"]:
    edge_data = edge_data.copy()

    # Separate the starting and ending entity names.
    source = edge_data.pop("source")
    target = edge_data.pop("target")

    # Recreate the edge with its relationship and evidence properties.
    reloaded_graph.add_edge(
        source,
        target,
        **edge_data,
    )

# Compare the original graph with the reloaded graph.
print("Original nodes:", graph.number_of_nodes())
print("Reloaded nodes:", reloaded_graph.number_of_nodes())

print("Original edges:", graph.number_of_edges())
print("Reloaded edges:", reloaded_graph.number_of_edges())

# Check that the node and edge counts have not changed.
assert (
    graph.number_of_nodes()
    == reloaded_graph.number_of_nodes()
)

assert (
    graph.number_of_edges()
    == reloaded_graph.number_of_edges()
)

# Check that a known relationship still exists.
assert reloaded_graph.has_edge("Alice", "SDI")

assert has_relationship(
    reloaded_graph,
    "Alice",
    "SDI",
    "WORKS_AT",
)

# Find Alice's node record in the JSON data.
alice_data = next(
    item
    for item in loaded_data["nodes"]
    if item["id"] == "Alice"
)

print("Alice in JSON:", alice_data)

# Find the Alice -> SDI edge record in the JSON data.
alice_sdi_edge = next(
    item
    for item in loaded_data["edges"]
    if (
        item["source"] == "Alice"
        and item["target"] == "SDI"
    )
)

print(
    "Alice -> SDI source document:",
    alice_sdi_edge["source_document_id"],
)

print("JSON reload validation passed.")

# We have now saved the graph, loaded it into a new graph,
# and checked that important data is still available.


# ============================================================
# 14. VISUALIZE THE COMPLETE KNOWLEDGE GRAPH
# ============================================================

print("\n" + "=" * 65)
print("10. VISUALIZE THE COMPLETE GRAPH")
print("=" * 65)

# Create a large drawing area so the graph has room to spread out.
plt.figure(figsize=(18, 12))

# spring_layout places connected nodes near each other.
# seed=42 makes the layout more consistent between runs.
positions = nx.spring_layout(
    graph,
    seed=42,
    k=1.5,
)

# Draw the entities as circles.
nx.draw_networkx_nodes(
    graph,
    positions,
    node_size=1800,
)

# Write the entity names inside or near the circles.
nx.draw_networkx_labels(
    graph,
    positions,
    font_size=7,
)

# Draw arrows to show the direction of each relationship.
nx.draw_networkx_edges(
    graph,
    positions,
    arrows=True,
    arrowsize=15,
    connectionstyle="arc3,rad=0.08",
)

# Create labels for the arrows.
# Each label shows the relationship type.
edge_labels = {
    (source, target): attributes["relation"]
    for source, target, attributes in graph.edges(data=True)
}

# Display relationship names next to the arrows.
nx.draw_networkx_edge_labels(
    graph,
    positions,
    edge_labels=edge_labels,
    font_size=6,
    label_pos=0.5,
)

plt.title("Complete Knowledge Graph")

# Hide the x-axis and y-axis because they are not important here.
plt.axis("off")

# Adjust spacing so that labels fit better.
plt.tight_layout()

# Choose where to save the graph image.
full_graph_path = OUTPUT_DIR / "knowledge_graph_full.png"

# Save the image as a high-resolution PNG.
plt.savefig(
    full_graph_path,
    dpi=200,
    bbox_inches="tight",
)

print("Complete graph image saved to:", full_graph_path)

# Close this figure so it does not interfere with the next one.
plt.close()


# ============================================================
# 15. CREATE A SMALL GRAPH WITH FIVE NODES AND SIX EDGES
# ============================================================

print("\n" + "=" * 65)
print("11. SMALL GRAPH VISUALIZATION")
print("=" * 65)

# Create a separate graph for a simpler example.
small_graph = nx.DiGraph()

# Define exactly five entities.
small_entities = {
    "Alice": {"entity_type": "Person"},
    "SDI": {"entity_type": "Organization"},
    "AI": {"entity_type": "TechnicalConcept"},
    "RAG": {"entity_type": "TechnicalConcept"},
    "Question Answering": {"entity_type": "Application"},
}

# Add the five entities to the smaller graph.
for node, properties in small_entities.items():
    small_graph.add_node(node, **properties)

# Define six relationships between those five entities.
small_relationships = [
    ("Alice", "SDI", "WORKS_AT"),
    ("Alice", "AI", "STUDIES"),
    ("AI", "RAG", "INCLUDES"),
    ("RAG", "Question Answering", "USED_IN"),
    ("AI", "Question Answering", "SUPPORTS"),
    ("SDI", "AI", "STUDIES"),
]

# Add the six relationships to the small graph.
for source, target, relation in small_relationships:
    small_graph.add_edge(
        source,
        target,
        relation=relation,
    )

# Check that the small graph has exactly five nodes and six edges.
assert small_graph.number_of_nodes() == 5
assert small_graph.number_of_edges() == 6

print("Small graph nodes:", small_graph.number_of_nodes())
print("Small graph edges:", small_graph.number_of_edges())

# Calculate positions for the five nodes.
small_positions = nx.spring_layout(
    small_graph,
    seed=42,
)

# Start drawing the small graph.
plt.figure(figsize=(11, 8))

# Draw the five entity circles.
nx.draw_networkx_nodes(
    small_graph,
    small_positions,
    node_size=2800,
)

# Display entity names.
nx.draw_networkx_labels(
    small_graph,
    small_positions,
    font_size=9,
)

# Draw directed arrows between entities.
nx.draw_networkx_edges(
    small_graph,
    small_positions,
    arrows=True,
    arrowsize=20,
    connectionstyle="arc3,rad=0.08",
)

# Get the relationship labels for the small graph.
small_edge_labels = {
    (source, target): attributes["relation"]
    for source, target, attributes
    in small_graph.edges(data=True)
}

# Show the relationship names on the drawing.
nx.draw_networkx_edge_labels(
    small_graph,
    small_positions,
    edge_labels=small_edge_labels,
    font_size=8,
)

plt.title("Small Knowledge Graph: Five Nodes and Six Edges")
plt.axis("off")
plt.tight_layout()

# Save the small graph image.
small_graph_path = OUTPUT_DIR / "knowledge_graph_small.png"

plt.savefig(
    small_graph_path,
    dpi=200,
    bbox_inches="tight",
)

print("Small graph image saved to:", small_graph_path)

# Display the remaining open figure, if the environment supports it.
plt.show()


# ============================================================
# 16. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("PRACTICAL EXERCISE COMPLETED")
print("=" * 65)

# Print the size of the main graph.
print("Main graph nodes:", graph.number_of_nodes())
print("Main graph edges:", graph.number_of_edges())

# Show the files generated by this program.
print("\nGenerated files:")
print("1.", json_path)
print("2.", full_graph_path)
print("3.", small_graph_path)

print("\nConcepts practiced:")
print("- Nodes and entity properties")
print("- Directed edges and relationship types")
print("- Triples")
print("- Incoming and outgoing neighbors")
print("- Shortest paths")
print("- Relationship validation")
print("- Source document IDs and evidence")
print("- JSON export and reload")
print("- Graph visualization")

