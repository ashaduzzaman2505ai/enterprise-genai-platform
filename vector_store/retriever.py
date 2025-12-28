from typing import List, Dict, Any, Optional

from embeddings.embedder_factory import get_embedder
from embeddings.base import BaseEmbedder
from vector_store.base import BaseVectorStore
from vector_store.faiss_store import FaissVectorStore


class Retriever:
    """Combines an embedder and vector store for text retrieval."""

    def __init__(self, embedder: Optional[BaseEmbedder] = None, store: Optional[BaseVectorStore] = None):
        self.embedder = embedder or get_embedder()
        self.store = store or FaissVectorStore(dim=384)  # Default dim for all-MiniLM

    def index(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> None:
        """Index texts by embedding them and adding to the store."""
        embeddings = self.embedder.embed(texts)
        self.store.add(embeddings, metadatas)

    def query(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the store with text and return top-k metadata."""
        query_embedding = self.embedder.embed([query_text])[0]
        return self.store.search(query_embedding, k)
