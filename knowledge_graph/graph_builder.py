import json
from pathlib import Path
from typing import Dict, Any

from common.config import settings
from common.logger import logger
from knowledge_graph.entity_extractor import extract_entities
from knowledge_graph.graph_client import GraphClient


class GraphBuilder:
    """Builds knowledge graph from document chunks."""

    def __init__(self, graph_client: GraphClient = None):
        self.graph = graph_client or GraphClient()

    def create_entity(self, entity: Dict[str, Any]) -> None:
        """Create or merge an entity node."""
        query = """
        MERGE (e:Entity {name: $name, type: $type})
        """
        self.graph.run(query, entity)

    def link_document(self, doc_id: str, entity_name: str) -> None:
        """Create relationship between document and entity."""
        query = """
        MATCH (d:Document {id: $doc_id})
        MATCH (e:Entity {name: $entity_name})
        MERGE (d)-[:MENTIONS]->(e)
        """
        self.graph.run(query, {
            "doc_id": doc_id,
            "entity_name": entity_name
        })

    def process_chunks(self, chunks_file: Path) -> None:
        """Process chunks file and build graph."""
        logger.info("Processing chunks from {}", chunks_file)

        try:
            with chunks_file.open("r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    try:
                        obj = json.loads(line.strip())
                        text = obj.get("content", "")
                        doc_id = f"doc_{i}"

                        # Create document node
                        self.graph.run(
                            "MERGE (d:Document {id: $id})",
                            {"id": doc_id}
                        )

                        entities = extract_entities(text)
                        for ent in entities:
                            self.create_entity(ent)
                            self.link_document(doc_id, ent["name"])

                    except json.JSONDecodeError as e:
                        logger.warning("Skipping invalid JSON at line {}: {}", i + 1, e)
                    except Exception as e:
                        logger.error("Error processing line {}: {}", i + 1, e)

        except FileNotFoundError:
            logger.error("Chunks file not found: {}", chunks_file)
            raise

        logger.info("Graph building completed")

    def close(self) -> None:
        """Close the graph connection."""
        if self.graph:
            self.graph.close()


if __name__ == "__main__":
    settings.ensure_data_dir()
    chunks_file = settings.DATA_DIR / "processed" / "chunks.jsonl"

    builder = GraphBuilder()
    try:
        builder.process_chunks(chunks_file)
    finally:
        builder.close()
