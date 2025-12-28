from typing import Optional

from embeddings.base import BaseEmbedder
from embeddings.hf_embedder import HuggingFaceEmbedder
from embeddings.openai_embedder import OpenAIEmbedder


def get_embedder(provider: str = "hf", **kwargs) -> BaseEmbedder:
    """Factory function to create an embedder instance.

    Args:
        provider: 'hf' for HuggingFace or 'openai' for OpenAI.
        **kwargs: Additional arguments passed to the embedder constructor.

    Returns:
        An instance of BaseEmbedder.

    Raises:
        ValueError: If provider is not supported.
    """
    if provider == "openai":
        return OpenAIEmbedder(**kwargs)
    elif provider == "hf":
        return HuggingFaceEmbedder(**kwargs)
    else:
        raise ValueError(f"Unsupported embedder provider: {provider}")
