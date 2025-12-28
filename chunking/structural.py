import re
from typing import List

from chunking.base import BaseChunker
from common.schemas import DocumentSchema
from chunking.tokenizer import TokenCounter
from chunking.semantic import SemanticChunker


class StructuralChunker(BaseChunker):
    """Chunk documents by structure (Markdown headers) and fall back to
    semantic chunking for large sections.
    """

    def __init__(self, max_tokens: int = 512) -> None:
        self.max_tokens = int(max_tokens)
        self.tokenizer = TokenCounter()

    def chunk(self, document: DocumentSchema) -> List[DocumentSchema]:
        # Split on markdown headers while keeping text content readable.
        sections = [s for s in re.split(r"\n#{1,6}\s+", document.content) if s.strip()]
        chunks: List[DocumentSchema] = []

        for section in sections:
            token_count = self.tokenizer.count(section)
            if token_count <= self.max_tokens:
                chunks.append(
                    DocumentSchema(
                        content=section.strip(),
                        metadata={
                            **document.metadata,
                            "chunk_type": "structural",
                            "token_count": token_count,
                        },
                    )
                )
            else:
                # Fallback: delegate to semantic chunker for overly large sections.
                chunks.extend(
                    SemanticChunker(self.max_tokens).chunk(
                        DocumentSchema(content=section, metadata=document.metadata)
                    )
                )

        return chunks
