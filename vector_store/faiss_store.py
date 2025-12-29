from typing import List, Dict, Any, Optional
from pathlib import Path

import faiss
import numpy as np

from vector_store.base import BaseVectorStore
from common.config import settings


class FaissVectorStore(BaseVectorStore):
    """Vector store using FAISS for efficient similarity search."""

    def __init__(self, dim: int, index_path: Optional[Path] = None):
        self.dim = dim
        self.index_path = index_path or settings.DATA_DIR / "vector_store" / "faiss.index"
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        else:
            self.index = faiss.IndexFlatL2(dim)
        
        self.metadatas: List[Dict[str, Any]] = []
        self.metadata_path = self.index_path.with_suffix('.metadata.json')
        if self.metadata_path.exists():
            import json
            with open(self.metadata_path, 'r') as f:
                self.metadatas = json.load(f)

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

    def save(self) -> None:
        """Save the index and metadata to disk."""
        faiss.write_index(self.index, str(self.index_path))
        import json
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadatas, f)
