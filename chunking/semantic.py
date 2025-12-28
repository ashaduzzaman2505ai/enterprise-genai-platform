import nltk
from typing import List

from nltk.tokenize import sent_tokenize
import re

from chunking.base import BaseChunker
from common.schemas import DocumentSchema
from chunking.tokenizer import TokenCounter


class SemanticChunker(BaseChunker):
    """Chunk documents by sentence while keeping chunks under a token limit.

    The class lazily ensures the NLTK punkt model is available to avoid
    forcing network access at import time in constrained environments.
    """

    def __init__(self, max_tokens: int = 512) -> None:
        self.max_tokens = int(max_tokens)
        self.tokenizer = TokenCounter()

        # Ensure NLTK Punkt tokenizer is available; do not download indiscriminately
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")

    def chunk(self, document: DocumentSchema) -> List[DocumentSchema]:
        """Return list of `DocumentSchema` chunks built from sentence boundaries.

        Behavior:
        - Accumulate sentences until the token count would exceed `max_tokens`.
        - Emit a chunk when the buffer reaches or exceeds the limit.
        - Remaining buffer is emitted as a final chunk.
        """
        # Prefer NLTK sentence tokenizer when available; fall back to a
        # lightweight regex-based splitter to avoid runtime errors in
        # environments without NLTK data installed.
        try:
            sentences = sent_tokenize(document.content)
        except LookupError:
            # Simple splitter: split on sentence-ending punctuation.
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', document.content.strip()) if s.strip()]
        chunks: List[DocumentSchema] = []
        buffer: List[str] = []

        for sentence in sentences:
            # If adding the sentence would exceed the limit, flush first.
            candidate = buffer + [sentence]
            candidate_text = " ".join(candidate)
            token_count = self.tokenizer.count(candidate_text)

            if token_count > self.max_tokens and buffer:
                content = " ".join(buffer)
                chunks.append(
                    DocumentSchema(
                        content=content,
                        metadata={
                            **document.metadata,
                            "chunk_type": "semantic",
                            "token_count": self.tokenizer.count(content),
                        },
                    )
                )
                buffer = [sentence]
            else:
                buffer.append(sentence)

        if buffer:
            content = " ".join(buffer)
            chunks.append(
                DocumentSchema(
                    content=content,
                    metadata={
                        **document.metadata,
                        "chunk_type": "semantic",
                        "token_count": self.tokenizer.count(content),
                    },
                )
            )

        return chunks
