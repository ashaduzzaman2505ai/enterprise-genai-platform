from typing import List, Optional
import os

from openai import OpenAI

from embeddings.base import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    """Embedder using OpenAI's embedding models."""

    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def embed(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [d.embedding for d in response.data]
        except Exception as e:
            raise RuntimeError(f"Failed to embed texts with OpenAI: {e}") from e
