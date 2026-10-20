
# Import json to save graph data in a JSON file.
import json

# Import Path to create folders and manage file paths.
from pathlib import Path

# Import matplotlib to draw and display the knowledge graph.
import matplotlib.pyplot as plt

# Import networkx to create and work with graphs.
import networkx as nx


# --------------------------------------------------
# 1. Create a directed graph
# --------------------------------------------------

# A graph contains nodes (entities) and edges (relationships).
# A directed graph means each relationship has a direction.
# For example: Alice -> SDI means Alice WORKS_AT SDI.
graph = nx.DiGraph()


# --------------------------------------------------
# 2. Define entities and their properties
# --------------------------------------------------

# Entities are the things we want to store in our graph.
# Each entity has a name and a type.
# For example, Alice is a Person and SDI is an Organization.
entities = {
    "Alice": {
        "entity_type": "Person",
    },
    "Bob": {
        "entity_type": "Person",
    },
    "SDI": {
        "entity_type": "Organization",
    },
    "Artificial Intelligence": {
        "entity_type": "TechnicalConcept",
    },
    "RAG": {
        "entity_type": "TechnicalConcept",
    },
    "GraphRAG": {
        "entity_type": "TechnicalConcept",
    },
    "Vector Database": {
        "entity_type": "TechnicalConcept",
    },
    "Embeddings": {
        "entity_type": "TechnicalConcept",
    },
    "Research Project": {
        "entity_type": "Project",
    },
    "Question Answering": {
        "entity_type": "Application",
    },
}


# --------------------------------------------------
# 3. Add nodes to the graph
# --------------------------------------------------

# Loop through all the entities.
# add_node() adds each entity to the graph.
# **properties attaches details such as entity_type to the node.
for entity_name, properties in entities.items():
    graph.add_node(
        entity_name,
        **properties,
    )


# --------------------------------------------------
# 4. Define relationships between entities
# --------------------------------------------------

# Each relationship contains four values:
# 1. Source: where the relationship starts.
# 2. Target: where the relationship points.
# 3. Relation: how the two entities are connected.
# 4. Document ID: the document that supports this relationship.
#
# Example:
# ("Alice", "SDI", "WORKS_AT", "doc_001")
# means Alice WORKS_AT SDI, according to doc_001.
relationships = [
    (
        "Alice",
        "SDI",
        "WORKS_AT",
        "doc_001",
    ),
    (
        "Bob",
        "SDI",
        "WORKS_AT",
        "doc_002",
    ),
    (
        "Alice",
        "Artificial Intelligence",
        "STUDIES",
        "doc_003",
    ),
    (
        "Bob",
        "Artificial Intelligence",
        "STUDIES",
        "doc_004",
    ),
    (
        "Artificial Intelligence",
        "RAG",
        "INCLUDES",
        "doc_005",
    ),
    (
        "Artificial Intelligence",
        "GraphRAG",
        "INCLUDES",
        "doc_006",
    ),
    (
        "RAG",
        "Embeddings",
        "USES",
        "doc_007",
    ),
    (
        "RAG",
        "Vector Database",
        "USES",
        "doc_008",
    ),
    (
        "GraphRAG",
        "RAG",
        "EXTENDS",
        "doc_009",
    ),
    (
        "GraphRAG",
        "Vector Database",
        "USES",
        "doc_010",
    ),
    (
        "GraphRAG",
        "Embeddings",
        "USES",
        "doc_011",
    ),
    (
        "Alice",
        "Research Project",
        "WORKS_ON",
        "doc_012",
    ),
    (
        "Bob",
        "Research Project",
        "WORKS_ON",
        "doc_013",
    ),
    (
        "Research Project",
        "GraphRAG",
        "STUDIES",
        "doc_014",
    ),
    (
        "RAG",
        "Question Answering",
        "USED_IN",
        "doc_015",
    ),
    (
        "GraphRAG",
        "Question Answering",
        "USED_IN",
        "doc_016",
    ),
]


# --------------------------------------------------
# 5. Add relationships and their properties
# --------------------------------------------------

# Loop through every relationship.
# add_edge() connects the source node to the target node.
# relation stores the relationship name.
# source_document_id records which document supports it.
for source, target, relation, document_id in relationships:
    graph.add_edge(
        source,
        target,
        relation=relation,
        source_document_id=document_id,
    )


# --------------------------------------------------
# 6. Print basic graph statistics
# --------------------------------------------------

# number_of_nodes() counts the entities.
# number_of_edges() counts the relationships.
print("KNOWLEDGE GRAPH STATISTICS")
print("-" * 40)

print("Number of nodes:", graph.number_of_nodes())
print("Number of edges:", graph.number_of_edges())


# --------------------------------------------------
# 7. Print graph triples
# --------------------------------------------------

# A triple is a simple way to represent a fact:
# (Subject, Relationship, Object)
#
# Example:
# (Alice, WORKS_AT, SDI)
#
# edges(data=True) gives us each connection and its properties.
print("\nKNOWLEDGE GRAPH TRIPLES")
print("-" * 40)

for source, target, attributes in graph.edges(data=True):
    # Get the relationship name from the edge properties.
    relation = attributes["relation"]

    print(
        f"({source}, {relation}, {target})"
    )


# --------------------------------------------------
# 8. Find direct outgoing neighbors
# --------------------------------------------------

# A neighbor is a node directly connected to another node.
# successors() returns nodes that this entity points to.
#
# For Alice, this should include:
# SDI, Artificial Intelligence, Research Project.
entity = "Alice"

print(f"\nDIRECT OUTGOING NEIGHBORS OF {entity}")
print("-" * 40)

neighbors = list(graph.successors(entity))

for neighbor in neighbors:
    print(neighbor)


# --------------------------------------------------
# 9. Find a path between two entities
# --------------------------------------------------

# A path is a sequence of connected nodes.
# shortest_path() finds a path with the fewest edges.
#
# Here, we check whether Alice can reach GraphRAG
# by following the graph's relationship directions.
source_entity = "Alice"
target_entity = "GraphRAG"

print(
    f"\nPATH FROM {source_entity} TO {target_entity}"
)
print("-" * 40)

try:
    path = nx.shortest_path(
        graph,
        source=source_entity,
        target=target_entity,
    )

    # Print the nodes in the path.
    print(" -> ".join(path))

    # Print the relationship used at each step.
    # zip(path, path[1:]) pairs each node with the next node.
    for source, target in zip(path, path[1:]):
        relation = graph[source][target]["relation"]

        print(
            f"{source} --{relation}--> {target}"
        )

except nx.NetworkXNoPath:
    # This happens if the nodes exist but no directed path connects them.
    print("No directed path exists between these entities.")

except nx.NodeNotFound as error:
    # This happens if a requested node is not in the graph.
    print("Entity not found:", error)


# --------------------------------------------------
# 10. Check whether an expected relationship exists
# --------------------------------------------------

# Check whether Alice WORKS_AT SDI.
# has_edge() checks whether Alice points directly to SDI.
# get("relation") checks whether that edge has the expected label.
source = "Alice"
target = "SDI"
expected_relation = "WORKS_AT"

relationship_exists = (
    graph.has_edge(source, target)
    and graph[source][target].get("relation")
    == expected_relation
)

print("\nRELATIONSHIP VALIDATION")
print("-" * 40)

# True means the expected relationship exists.
# False means it does not exist as specified.
print(
    f"{source} --{expected_relation}--> {target}: "
    f"{relationship_exists}"
)


# --------------------------------------------------
# 11. Inspect node properties
# --------------------------------------------------

# Nodes can store extra information called properties or attributes.
# For example, Alice has entity_type="Person".
# nodes(data=True) returns each node and its properties.
print("\nNODE PROPERTIES")
print("-" * 40)

for node, attributes in graph.nodes(data=True):
    print(node, attributes)


# --------------------------------------------------
# 12. Inspect relationship properties
# --------------------------------------------------

# Edges can also store properties.
# In this example, each edge stores:
# - relation: the type of connection
# - source_document_id: the supporting document's ID
print("\nEDGE PROPERTIES")
print("-" * 40)

for source, target, attributes in graph.edges(data=True):
    print(
        source,
        "->",
        target,
        attributes,
    )


# --------------------------------------------------
# 13. Export graph data to JSON
# --------------------------------------------------

# Create a folder to store the graph output files.
# parents=True creates any missing parent folders.
# exist_ok=True avoids an error if the folder already exists.
output_directory = Path("data/graph_examples")
output_directory.mkdir(
    parents=True,
    exist_ok=True,
)

# Convert the graph into a dictionary.
# "nodes" stores entities and their properties.
# "edges" stores connections and their properties.
# This format is easy to save, inspect, and share.
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

# Choose the file path for the JSON output.
json_path = output_directory / "knowledge_graph.json"

# Open the file and write the graph data into it.
# indent=2 makes the JSON easier for humans to read.
# ensure_ascii=False preserves non-English characters.
with json_path.open("w", encoding="utf-8") as file:
    json.dump(
        graph_data,
        file,
        indent=2,
        ensure_ascii=False,
    )

print("\nGraph JSON saved to:", json_path)


# --------------------------------------------------
# 14. Draw and save the knowledge graph
# --------------------------------------------------

# Create a large drawing area for the graph.
plt.figure(figsize=(15, 10))

# spring_layout() positions nodes so the graph is easier to view.
# seed=42 keeps the layout consistent between runs.
positions = nx.spring_layout(
    graph,
    seed=42,
    k=1.2,
)

# Draw the nodes (entities) as circles.
nx.draw_networkx_nodes(
    graph,
    positions,
    node_size=2400,
)

# Display each entity's name beside its node.
nx.draw_networkx_labels(
    graph,
    positions,
    font_size=8,
)

# Draw arrows to show the direction of each relationship.
nx.draw_networkx_edges(
    graph,
    positions,
    arrows=True,
    arrowsize=18,
    connectionstyle="arc3,rad=0.08",
)

# Create labels for the edges using their relationship names.
# For example, the arrow from Alice to SDI is labeled WORKS_AT.
edge_labels = {
    (source, target): attributes["relation"]
    for source, target, attributes in graph.edges(data=True)
}

# Display the relationship names beside the arrows.
nx.draw_networkx_edge_labels(
    graph,
    positions,
    edge_labels=edge_labels,
    font_size=7,
    label_pos=0.5,
)

# Add a title and hide the x/y axes because they are not important here.
plt.title("Knowledge Graph: Entities and Relationships")
plt.axis("off")

# Adjust spacing so labels and nodes fit better.
plt.tight_layout()

# Save the graph drawing as an image file.
image_path = output_directory / "knowledge_graph.png"

plt.savefig(
    image_path,
    dpi=200,
    bbox_inches="tight",
)

print("Graph image saved to:", image_path)

# Open a window showing the graph drawing.
plt.show()
