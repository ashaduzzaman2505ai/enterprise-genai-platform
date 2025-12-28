from ingestion.parsers.cleaner import clean_text
from ingestion.metadata.enrich import enrich_metadata


def test_clean_text_normalization():
    raw = "This\t is  text\nwith" + chr(0) + "null and" + chr(0) + " combining\u0301"
    cleaned = clean_text(raw)
    assert "\x00" not in cleaned
    assert "  " not in cleaned


def test_enrich_metadata_non_mutating():
    base = {"a": 1}
    out = enrich_metadata(base)
    assert out.get("ingested_at") is not None
    # original dict should not be mutated
    assert "ingested_at" not in base
