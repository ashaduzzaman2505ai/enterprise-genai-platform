import os
from tqdm import tqdm
from common.logger import logger
from ingestion.loaders.pdf_loader import load_pdf
from ingestion.loaders.text_loader import load_text
from ingestion.parsers.cleaner import clean_text
from ingestion.metadata.enrich import enrich_metadata

RAW_DIR = "data/raw"
OUT_DIR = "data/processed"

os.makedirs(OUT_DIR, exist_ok=True)

def ingest():
    documents = []

    for file in tqdm(os.listdir(RAW_DIR)):
        path = os.path.join(RAW_DIR, file)

        if file.endswith(".pdf"):
            docs = load_pdf(path)
        elif file.endswith(".txt") or file.endswith(".md"):
            docs = load_text(path)
        else:
            continue

        for doc in docs:
            doc.content = clean_text(doc.content)
            doc.metadata = enrich_metadata(doc.metadata)
            documents.append(doc)

    logger.info(f"Ingested {len(documents)} documents")

    # Save as JSONL (standard practice)
    with open(os.path.join(OUT_DIR, "documents.jsonl"), "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(doc.model_dump_json() + "\n")

if __name__ == "__main__":
    ingest()
