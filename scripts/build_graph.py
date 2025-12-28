"""Script to build knowledge graph from chunks."""

from pathlib import Path

from common.config import settings
from common.logger import logger
from knowledge_graph.graph_builder import GraphBuilder


def main():
    settings.ensure_data_dir()
    chunks_file = settings.DATA_DIR / "processed" / "chunks.jsonl"

    if not chunks_file.exists():
        logger.error("Chunks file not found: {}", chunks_file)
        return

    logger.info("Building knowledge graph from {}", chunks_file)

    builder = GraphBuilder()
    try:
        builder.process_chunks(chunks_file)
        logger.info("Knowledge graph built successfully")
    except Exception as e:
        logger.error("Failed to build knowledge graph: {}", e)
        raise
    finally:
        builder.close()


if __name__ == "__main__":
    main()