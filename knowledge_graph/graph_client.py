from typing import Any, Optional
import os

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class GraphClient:
    """Client for interacting with Neo4j graph database."""

    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")

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
                return session.run(query, params or {})
        except Exception as e:
            raise RuntimeError(f"Failed to execute query: {e}") from e
