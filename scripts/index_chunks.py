"""Script to index chunked documents into a vector store."""

import json
from pathlib import Path

from common.config import settings
from common.logger import logger
from vector_store.retriever import Retriever


def load_chunks(chunks_file: Path):
    """Load texts and metadatas from chunks JSONL file."""
    texts = []
    metadatas = []
    try:
        with chunks_file.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    obj = json.loads(line.strip())
                    texts.append(obj["content"])
                    metadatas.append(obj["metadata"])
                except json.JSONDecodeError as e:
                    logger.warning("Skipping invalid JSON at line {}: {}", line_num, e)
    except FileNotFoundError:
        logger.error("Chunks file not found: {}", chunks_file)
        raise
    return texts, metadatas


def main():
    chunks_file = settings.DATA_DIR / "processed" / "chunks.jsonl"
    settings.ensure_data_dir()

    logger.info("Loading chunks from {}", chunks_file)
    texts, metadatas = load_chunks(chunks_file)

    if not texts:
        logger.warning("No chunks to index")
        return

    logger.info("Indexing {} chunks", len(texts))

    # Change provider here: "hf" or "openai"
    from embeddings.embedder_factory import get_embedder
    embedder = get_embedder("hf")  # or "openai"
    retriever = Retriever(embedder=embedder)
    retriever.index(texts, metadatas)

    # Save the index
    retriever.store.save()

    # Test search
    test_query = "What is the compliance policy?"
    logger.info("Testing query: {}", test_query)
    results = retriever.query(test_query, k=5)
    for i, r in enumerate(results, 1):
        logger.info("Result {}: {}", i, r)
    


if __name__ == "__main__":
    main()
