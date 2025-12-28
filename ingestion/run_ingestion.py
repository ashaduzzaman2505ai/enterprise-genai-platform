from __future__ import annotations

from pathlib import Path
from typing import List

from tqdm import tqdm

from common.config import settings
from common.logger import logger
from ingestion.loaders.pdf_loader import load_pdf
from ingestion.loaders.text_loader import load_text
from ingestion.parsers.cleaner import clean_text
from ingestion.metadata.enrich import enrich_metadata
from common.schemas import DocumentSchema


RAW_DIR = settings.DATA_DIR / "raw"
OUT_DIR = settings.DATA_DIR / "processed"


def _serialize_doc(doc: DocumentSchema) -> str:
    if hasattr(doc, "model_dump_json"):
        return doc.model_dump_json()
    return doc.json()


def ingest() -> List[DocumentSchema]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    documents: List[DocumentSchema] = []

    for file in tqdm(list(RAW_DIR.iterdir()) if RAW_DIR.exists() else []):
        path = file
        if path.suffix.lower() == ".pdf":
            docs = load_pdf(path)
        elif path.suffix.lower() in {".txt", ".md"}:
            docs = load_text(path)
        else:
            continue

        for doc in docs:
            doc.content = clean_text(doc.content)
            doc.metadata = enrich_metadata(doc.metadata)
            documents.append(doc)

    logger.info("Ingested %d documents", len(documents))

    out_path = OUT_DIR / "documents.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for doc in documents:
            f.write(_serialize_doc(doc) + "\n")

    return documents


if __name__ == "__main__":
    ingest()
