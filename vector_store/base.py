from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseVectorStore(ABC):
    """Abstract base class for vector stores.

    Implementations should provide methods to add vectors with metadata
    and search for similar vectors.
    """

    @abstractmethod
    def add(self, embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        """Add embeddings with associated metadata to the store.

        Args:
            embeddings: List of embedding vectors.
            metadatas: List of metadata dictionaries, one per embedding.
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query_embedding: List[float], k: int) -> List[Dict[str, Any]]:
        """Search for the k most similar embeddings.

        Args:
            query_embedding: The query vector.
            k: Number of results to return.

        Returns:
            List of metadata dictionaries for the top-k matches.
        """
        raise NotImplementedError
