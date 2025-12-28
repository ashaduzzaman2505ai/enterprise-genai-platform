from abc import ABC, abstractmethod
from typing import List

from common.schemas import DocumentSchema


class BaseChunker(ABC):
    """Abstract base class for document chunkers.

    Implementations should return a list of `DocumentSchema` instances
    representing logical chunks of the input document.
    """

    @abstractmethod
    def chunk(self, document: DocumentSchema) -> List[DocumentSchema]:
        """Split `document` into smaller documents (chunks).

        Returns:
            List[DocumentSchema]: list of chunk documents.
        """
        raise NotImplementedError
