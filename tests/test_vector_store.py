from vector_store.faiss_store import FaissVectorStore
from vector_store.retriever import Retriever


def test_faiss_store():
    store = FaissVectorStore(dim=2)
    embeddings = [[1.0, 0.0], [0.0, 1.0]]
    metadatas = [{"id": 1}, {"id": 2}]
    store.add(embeddings, metadatas)

    results = store.search([1.0, 0.0], k=1)
    assert len(results) == 1
    assert results[0]["id"] == 1


def test_retriever():
    retriever = Retriever(store=FaissVectorStore(dim=384))
    texts = ["Test document"]
    metadatas = [{"source": "test"}]
    retriever.index(texts, metadatas)

    results = retriever.query("test query", k=1)
    assert len(results) == 1
    assert results[0]["source"] == "test"