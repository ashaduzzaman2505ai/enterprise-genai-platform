"""Query functions for the knowledge graph."""

from typing import List, Dict, Any, Optional

from knowledge_graph.graph_client import GraphClient


class GraphQueries:
    """Collection of common graph queries."""

    def __init__(self, graph_client: Optional[GraphClient] = None):
        self.graph = graph_client or GraphClient()

    def find_related_entities(self, entity_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find entities related to the given entity."""
        query = """
        MATCH (e1:Entity {name: $name})-[r]-(e2:Entity)
        RETURN e2.name AS name, e2.type AS type, type(r) AS relation
        LIMIT $limit
        """
        result = self.graph.run(query, {"name": entity_name, "limit": limit})
        return [record.data() for record in result]

    def find_documents_mentioning(self, entity_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find documents that mention the given entity."""
        query = """
        MATCH (d:Document)-[:MENTIONS]->(e:Entity {name: $name})
        RETURN d.id AS doc_id
        LIMIT $limit
        """
        result = self.graph.run(query, {"name": entity_name, "limit": limit})
        return [record.data() for record in result]

    def get_entity_types(self) -> List[str]:
        """Get all unique entity types in the graph."""
        query = "MATCH (e:Entity) RETURN DISTINCT e.type AS type"
        result = self.graph.run(query)
        return [record["type"] for record in result]

    def close(self):
        """Close the graph connection."""
        if self.graph:
            self.graph.close()


# Example usage:
# queries = GraphQueries()
# related = queries.find_related_entities("Policy Data Retention")
# queries.close()
