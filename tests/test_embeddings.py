from unittest.mock import patch
from embeddings.hf_embedder import HuggingFaceEmbedder
from embeddings.openai_embedder import OpenAIEmbedder
from embeddings.embedder_factory import get_embedder


def test_hf_embedder():
    embedder = HuggingFaceEmbedder()
    texts = ["Hello world", "Test text"]
    embeddings = embedder.embed(texts)
    assert len(embeddings) == 2
    assert isinstance(embeddings[0], list)
    assert len(embeddings[0]) > 0


def test_openai_embedder_missing_key():
    with patch.dict('os.environ', {}, clear=True):
        try:
            embedder = OpenAIEmbedder(api_key=None)
            assert False, "Should raise ValueError"
        except ValueError:
            pass


def test_embedder_factory():
    hf = get_embedder("hf")
    assert isinstance(hf, HuggingFaceEmbedder)

    with patch.dict('os.environ', {'OPENAI_API_KEY': 'fake'}, clear=True):
        openai = get_embedder("openai")
        assert isinstance(openai, OpenAIEmbedder)

    try:
        get_embedder("invalid")
        assert False
    except ValueError:
        pass