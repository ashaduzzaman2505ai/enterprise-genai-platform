from knowledge_graph.entity_extractor import extract_entities
from knowledge_graph.schema import ENTITY_TYPES


def test_extract_entities():
    text = "The Data Retention Policy must be followed by the Security Team."
    entities = extract_entities(text)

    assert len(entities) > 0
    # Should find "Data Retention Policy" and "Security Team"
    entity_names = [e["name"] for e in entities]
    assert any("Policy" in name for name in entity_names)
    assert any("Team" in name for name in entity_names)

    for ent in entities:
        assert "type" in ent
        assert "name" in ent
        assert ent["type"] in ENTITY_TYPES


def test_extract_entities_empty():
    entities = extract_entities("")
    assert entities == []


def test_extract_entities_invalid():
    entities = extract_entities(None)
    assert entities == []