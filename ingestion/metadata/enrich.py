from datetime import datetime

def enrich_metadata(metadata: dict) -> dict:
    metadata["ingested_at"] = datetime.utcnow().isoformat()
    return metadata
