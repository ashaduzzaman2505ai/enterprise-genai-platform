from PyPDF2 import PdfReader
from common.schemas import DocumentSchema

def load_pdf(path: str) -> list[DocumentSchema]:
    reader = PdfReader(path)
    docs = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            docs.append(
                DocumentSchema(
                    content=text,
                    metadata={
                        "source": path,
                        "page": page_num
                    }
                )
            )
    return docs
