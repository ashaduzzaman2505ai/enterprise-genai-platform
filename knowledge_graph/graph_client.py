from typing import Any, Optional
import os

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from common.config import settings


class GraphClient:
    """Client for interacting with Neo4j graph database."""

    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.uri = uri or settings.NEO4J_URI or os.getenv("NEO4J_URI", "neo4j+s://your-instance.databases.neo4j.io")
        self.user = user or settings.NEO4J_USER or os.getenv("NEO4J_USER", "")
        self.password = password or settings.NEO4J_PASSWORD or os.getenv("NEO4J_PASSWORD", "")

        if not self.uri or not self.user or not self.password:
            raise ValueError(
                "Neo4j connection requires URI, USER, and PASSWORD. "
                "Set NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD environment variables "
                "or configure them in your settings."
            )

        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            self.driver.verify_connectivity()
        except ServiceUnavailable as e:
            raise ConnectionError(f"Failed to connect to Neo4j at {self.uri}: {e}") from e

    def close(self) -> None:
        """Close the database connection."""
        if hasattr(self, 'driver'):
            self.driver.close()

    def run(self, query: str, params: Optional[dict] = None):
        """Execute a Cypher query.

        Args:
            query: The Cypher query string.
            params: Parameters for the query.

        Returns:
            Query result object.
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                # Consume the result immediately to avoid consumption issues
                records = [record for record in result]
                return records
        except Exception as e:
            raise RuntimeError(f"Failed to execute query: {e}") from e
