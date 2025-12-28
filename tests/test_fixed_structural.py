from chunking.fixed import FixedChunker
from chunking.structural import StructuralChunker
from common.schemas import DocumentSchema


def test_fixed_chunker_basic():
    text = "word " * 200
    doc = DocumentSchema(content=text.strip(), metadata={"source": "test"})
    chunker = FixedChunker(max_tokens=50, overlap=5)
    chunks = chunker.chunk(doc)

    assert len(chunks) >= 3
    total_words = sum(len(c.content.split()) for c in chunks)
    assert total_words >= 200


def test_structural_chunker_basic():
    text = "# Heading\n" + "Paragraph one. " * 10 + "\n## Sub\n" + "Another. " * 30
    doc = DocumentSchema(content=text, metadata={"source": "test"})
    chunker = StructuralChunker(max_tokens=40)
    chunks = chunker.chunk(doc)

    assert len(chunks) >= 2
    for c in chunks:
        assert c.metadata.get("chunk_type") in {"structural", "semantic"}
        assert isinstance(c.content, str)
