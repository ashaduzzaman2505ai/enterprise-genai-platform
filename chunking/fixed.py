from typing import List
from pathlib import Path

from chunking.base import BaseChunker
from common.schemas import DocumentSchema
from chunking.tokenizer import TokenCounter


class FixedChunker(BaseChunker):
    """Create fixed-size chunks with optional token overlap.

    This implementation measures chunk size using `TokenCounter` so the
    `max_tokens` parameter refers to token counts rather than raw words.
    """

    def __init__(self, max_tokens: int = 512, overlap: int = 50) -> None:
        self.max_tokens = int(max_tokens)
        self.overlap = max(0, int(overlap))
        self.tokenizer = TokenCounter()

    def chunk(self, document: DocumentSchema) -> List[DocumentSchema]:
        words = document.content.split()
        chunks: List[DocumentSchema] = []

        n = len(words)
        start = 0

        while start < n:
            # Find the smallest `end` such that token_count >= max_tokens or end==n
            end = start + 1
            while end <= n:
                candidate = " ".join(words[start:end])
                token_count = self.tokenizer.count(candidate)
                if token_count >= self.max_tokens or end == n:
                    break
                end += 1

            content = " ".join(words[start:end])
            chunks.append(
                DocumentSchema(
                    content=content,
                    metadata={
                        **document.metadata,
                        "chunk_type": "fixed",
                        "token_count": self.tokenizer.count(content),
                    },
                )
            )

            # Advance start with overlap; ensure progress
            start = max(end - self.overlap, end if end == start else start + 1)

        return chunks
