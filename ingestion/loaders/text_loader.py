from typing import List
from pathlib import Path

from common.schemas import DocumentSchema


def load_text(path: Path) -> List[DocumentSchema]:
    with path.open("r", encoding="utf-8") as f:
        text = f.read()

    return [
        DocumentSchema(
            content=text,
            metadata={"source": str(path)}
        )
    ]
