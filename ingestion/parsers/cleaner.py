import re
import unicodedata
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """Normalize and clean raw text.

    - Normalize unicode to NFC
    - Replace multiple whitespace with single space
    - Remove null characters
    - Strip leading/trailing whitespace
    """
    if not text:
        return ""

    # Normalize unicode to avoid combining-character surprises
    normalized = unicodedata.normalize("NFC", text)
    # Collapse whitespace
    collapsed = re.sub(r"\s+", " ", normalized)
    # Remove nulls
    collapsed = collapsed.replace("\x00", "")
    return collapsed.strip()
