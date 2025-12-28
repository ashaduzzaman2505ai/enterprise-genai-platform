from chunking.semantic import SemanticChunker
from common.schemas import DocumentSchema


def test_semantic_chunker_basic():
    text = "This is sentence one. This is sentence two. " \
        "Here comes sentence three. And finally sentence four."
    doc = DocumentSchema(content=text, metadata={"source": "test"})
    chunker = SemanticChunker(max_tokens=10)
    chunks = chunker.chunk(doc)

    assert len(chunks) >= 2
    # Ensure metadata preserved and chunk_type set
    for c in chunks:
        assert c.metadata.get("source") == "test"
        assert c.metadata.get("chunk_type") == "semantic"
        assert isinstance(c.content, str)


def test_semantic_chunker_empty():
    doc = DocumentSchema(content="", metadata={})
    chunker = SemanticChunker(max_tokens=50)
    chunks = chunker.chunk(doc)
    assert chunks == [] or (len(chunks) == 1 and chunks[0].content == "")
