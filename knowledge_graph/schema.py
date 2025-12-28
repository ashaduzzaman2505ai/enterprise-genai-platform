"""Knowledge graph schema definitions."""

from typing import List


# Supported entity types for extraction and classification
ENTITY_TYPES: List[str] = [
    "Policy",
    "Regulation",
    "Team",
    "System",
    "Person",
    "Concept"
]

# Supported relationship types between entities
RELATION_TYPES: List[str] = [
    "MENTIONS",
    "RELATED_TO",
    "OWNED_BY",
    "DEPENDS_ON",
    "GOVERNS"
]

# Node labels used in the graph
NODE_LABELS: List[str] = [
    "Entity",
    "Document",
    "Chunk"
]
