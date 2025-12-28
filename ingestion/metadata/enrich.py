from datetime import datetime
from typing import Dict, Any


def enrich_metadata(metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return a new metadata dict with ingestion timestamp without mutating input."""
    base = dict(metadata or {})
    base["ingested_at"] = datetime.utcnow().isoformat()
    return base
