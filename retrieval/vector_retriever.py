import json
import faiss
import numpy as np
from typing import List, Dict, Any, Optional
from pathlib import Path

from sentence_transformers import SentenceTransformer

from retrieval.base import BaseRetriever
from common.config import settings
from common.logger import logger


class VectorRetriever(BaseRetriever):
    """Retriever using vector similarity search with FAISS."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        index_path: Optional[Path] = None,
        chunks_path: Optional[Path] = None
    ):
        self.model_name = model_name
        self.index_path = index_path or settings.DATA_DIR / "vector_store" / "faiss.index"
        self.chunks_path = chunks_path or settings.DATA_DIR / "processed" / "chunks.jsonl"

        try:
            self.model = SentenceTransformer(model_name)
            self.index = faiss.read_index(str(self.index_path))
            self.texts = self._load_texts()
            logger.info(f"Loaded vector retriever with {len(self.texts)} chunks")
        except Exception as e:
            logger.error(f"Failed to initialize VectorRetriever: {e}")
            raise

    def _load_texts(self) -> List[str]:
        """Load text chunks from JSONL file."""
        texts = []
        try:
            with open(self.chunks_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        texts.append(data.get("content", ""))
        except FileNotFoundError:
            logger.warning(f"Chunks file not found: {self.chunks_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing chunks file: {e}")
            raise
        return texts

    def retrieve(self, query: str, top_k: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Retrieve top-k similar chunks for the query.

        Args:
            query: The search query.
            top_k: Number of results to return.
            **kwargs: Additional parameters (ignored).

        Returns:
            List of result dictionaries with content and scores.
        """
        try:
            query_emb = self.model.encode([query])
            scores, indices = self.index.search(np.array(query_emb), top_k)

            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.texts):  # Safety check
                    results.append({
                        "source": "vector",
                        "score": float(scores[0][i]),
                        "content": self.texts[idx],
                        "index": int(idx)
                    })
            return results
        except Exception as e:
            logger.error(f"Error during vector retrieval: {e}")
            return []
