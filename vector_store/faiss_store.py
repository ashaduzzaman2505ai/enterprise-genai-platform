from typing import List, Dict, Any

import faiss
import numpy as np

from vector_store.base import BaseVectorStore


class FaissVectorStore(BaseVectorStore):
    """Vector store using FAISS for efficient similarity search."""

    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadatas: List[Dict[str, Any]] = []

    def add(self, embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        if len(embeddings) != len(metadatas):
            raise ValueError("Number of embeddings must match number of metadatas")
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadatas.extend(metadatas)

    def search(self, query_embedding: List[float], k: int) -> List[Dict[str, Any]]:
        query = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.metadatas):
                results.append(self.metadatas[idx])
        return results
