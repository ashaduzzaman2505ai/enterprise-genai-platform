from typing import List

from sentence_transformers import SentenceTransformer

from embeddings.base import BaseEmbedder


class HuggingFaceEmbedder(BaseEmbedder):
    """Embedder using HuggingFace Sentence Transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load SentenceTransformer model '{model_name}': {e}") from e

    def embed(self, texts: List[str]) -> List[List[float]]:
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            raise RuntimeError(f"Failed to embed texts with HuggingFace: {e}") from e
