from typing import List
from pathlib import Path

from PyPDF2 import PdfReader

from common.schemas import DocumentSchema


def load_pdf(path: Path) -> List[DocumentSchema]:
    try:
        reader = PdfReader(str(path))
    except Exception:
        return []

    docs: List[DocumentSchema] = []

    for page_num, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        if text.strip():
            docs.append(
                DocumentSchema(
                    content=text,
                    metadata={
                        "source": str(path),
                        "page": page_num,
                    },
                )
            )

    return docs
