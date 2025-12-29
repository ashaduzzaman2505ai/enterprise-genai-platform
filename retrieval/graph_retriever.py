from typing import List, Dict, Any

from knowledge_graph.graph_client import GraphClient
from retrieval.base import BaseRetriever
from common.logger import logger


class GraphRetriever(BaseRetriever):
    """Retriever using graph-based entity relationships."""

    def __init__(self, graph_client: GraphClient = None):
        self.graph = graph_client or GraphClient()

    def retrieve(self, query: str, entities: List[str] = None, depth: int = 2, **kwargs) -> List[Dict[str, Any]]:
        """Retrieve related entities from the knowledge graph.

        Args:
            query: The search query (used if entities not provided).
            entities: List of entity names to expand. If None, uses query as single entity.
            depth: Depth of relationship traversal.
            **kwargs: Additional parameters (ignored).

        Returns:
            List of related entity dictionaries.
        """
        if entities is None:
            entities = [query]  # Simple fallback

        results = []
        for entity in entities:
            try:
                cypher_query = f"""
                MATCH (e:Entity {{name: $name}})-[:MENTIONS*1..{depth}]-(n:Entity)
                WHERE n <> e
                RETURN DISTINCT n.name AS name, n.type AS type, '' AS description
                """
                records = self.graph.run(cypher_query, {
                    "name": entity
                })

                for record in records:
                    results.append({
                        "source": "graph",
                        "entity": entity,
                        "related": record["name"],
                        "type": record["type"],
                        "description": record.get("description", ""),
                        "relationship": f"{entity} -> {record['name']}"
                    })
            except Exception as e:
                logger.error(f"Error retrieving graph data for entity '{entity}': {e}")
                continue

        return results
