from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseRetriever(ABC):
    """Abstract base class for retrievers.

    Implementations should provide methods to retrieve relevant information
    based on a query.
    """

    @abstractmethod
    def retrieve(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """Retrieve relevant information for the given query.

        Args:
            query: The search query.
            **kwargs: Additional parameters for retrieval.

        Returns:
            List of result dictionaries.
        """
        raise NotImplementedError