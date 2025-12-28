from common.schemas import DocumentSchema

def load_text(path: str) -> list[DocumentSchema]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    return [
        DocumentSchema(
            content=text,
            metadata={"source": path}
        )
    ]
