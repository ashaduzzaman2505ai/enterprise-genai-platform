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

    def get_entity_count(self) -> int:
        """Get total number of entities in the graph."""
        query = "MATCH (e:Entity) RETURN count(e) AS count"
        result = self.graph.run(query)
        return result[0]["count"] if result else 0

    def get_document_count(self) -> int:
        """Get total number of documents in the graph."""
        query = "MATCH (d:Document) RETURN count(d) AS count"
        result = self.graph.run(query)
        return result[0]["count"] if result else 0

    def get_relationship_count(self) -> int:
        """Get total number of relationships in the graph."""
        query = "MATCH ()-[r]-() RETURN count(r) AS count"
        result = self.graph.run(query)
        return result[0]["count"] if result else 0

    def get_entity_types(self) -> List[str]:
        """Get all unique entity types in the graph."""
        query = "MATCH (e:Entity) RETURN DISTINCT e.type AS type"
        result = self.graph.run(query)
        return [record["type"] for record in result]

    def list_entities(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List entities with their types."""
        query = """
        MATCH (e:Entity)
        RETURN e.name AS name, e.type AS type
        ORDER BY e.name
        LIMIT $limit
        """
        result = self.graph.run(query, {"limit": limit})
        return [record.data() for record in result]

    def get_graph_stats(self) -> Dict[str, Any]:
        """Get comprehensive graph statistics."""
        return {
            "entities": self.get_entity_count(),
            "documents": self.get_document_count(),
            "relationships": self.get_relationship_count(),
            "entity_types": self.get_entity_types(),
        }


    def close(self):
        """Close the graph connection."""
        if self.graph:
            self.graph.close()


# # Example usage:
# queries = GraphQueries()
# related = queries.find_related_entities("Energy Policy Data")
# queries.close()
