import re
from typing import List, Dict, Any, Optional

from knowledge_graph.schema import ENTITY_TYPES


def extract_entities(text: str) -> List[Dict[str, Any]]:
    """Extract entities from text using rule-based patterns.

    This is a lightweight implementation that can be replaced with
    LLM-based extraction for better accuracy.

    Args:
        text: The text to extract entities from.

    Returns:
        List of entity dictionaries with 'type' and 'name' keys.
    """
    if not text or not isinstance(text, str):
        return []

    entities: List[Dict[str, Any]] = []

    # Define patterns for each entity type
    patterns = {
        "Policy": r"\bPolicy\s+[A-Z][a-zA-Z\s]+\b",
        "Regulation": r"\bRegulation\s+[A-Z][a-zA-Z\s]+\b",
        "System": r"\b[A-Z][a-zA-Z]+\s+System\b",
        "Team": r"\b[A-Z][a-zA-Z]+\s+Team\b",
        "Person": r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b",  # Simple name pattern
        "Concept": r"\b[A-Z][a-zA-Z\s]{3,}\b",  # Generic capitalized terms
    }

    for entity_type, pattern in patterns.items():
        try:
            matches = re.findall(pattern, text)
            for match in matches:
                name = match.strip()
                if name and len(name) > 2:  # Avoid very short matches
                    entities.append({
                        "type": entity_type,
                        "name": name
                    })
        except re.error:
            # Skip invalid patterns
            continue

    # Remove duplicates while preserving order
    seen = set()
    unique_entities = []
    for ent in entities:
        key = (ent["type"], ent["name"])
        if key not in seen:
            seen.add(key)
            unique_entities.append(ent)

    return unique_entities
