"""Ingestion package public API."""

from .loaders.pdf_loader import load_pdf
from .loaders.text_loader import load_text
from .parsers.cleaner import clean_text
from .metadata.enrich import enrich_metadata
from .run_ingestion import ingest

__all__ = [
	"load_pdf",
	"load_text",
	"clean_text",
	"enrich_metadata",
	"ingest",
]
