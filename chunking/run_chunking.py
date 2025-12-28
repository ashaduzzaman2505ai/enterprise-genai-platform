from __future__ import annotations

from pathlib import Path
from typing import Iterable, Dict

from tqdm import tqdm

from common.config import settings
from common.logger import logger
from common.schemas import DocumentSchema

from chunking.fixed import FixedChunker
from chunking.semantic import SemanticChunker
from chunking.structural import StructuralChunker


INPUT = settings.DATA_DIR / "processed" / "documents.jsonl"
OUTPUT = settings.DATA_DIR / "processed" / "chunks.jsonl"


def _serialize_doc(doc: DocumentSchema) -> str:
    # Compatible with both Pydantic v1 and v2
    if hasattr(doc, "model_dump_json"):
        return doc.model_dump_json()
    return doc.model_dump_json()


def load_docs(path: Path) -> Iterable[DocumentSchema]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                yield DocumentSchema.model_validate_json(line)
            except Exception:
                logger.exception("Failed to parse document line; skipping")


def run(selected: Dict[str, bool] | None = None) -> None:
    """Run chunking for all documents in the processed data directory.

    Args:
        selected: optional mapping of chunker names to enable/disable.
    """
    settings.ensure_data_dir()

    chunkers = {
        "fixed": FixedChunker(),
        "semantic": SemanticChunker(),
        "structural": StructuralChunker(),
    }

    if selected is None:
        selected = {k: True for k in chunkers}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    if not INPUT.exists():
        logger.warning("No input documents found at %s", INPUT)
        return

    with OUTPUT.open("w", encoding="utf-8") as out:
        for doc in tqdm(list(load_docs(INPUT))):
            for name, chunker in chunkers.items():
                if not selected.get(name, True):
                    continue
                for c in chunker.chunk(doc):
                    out.write(_serialize_doc(c) + "\n")


if __name__ == "__main__":
    run()
