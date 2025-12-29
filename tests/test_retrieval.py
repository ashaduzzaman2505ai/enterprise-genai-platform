import pytest
from unittest.mock import Mock, patch, mock_open

from retrieval.vector_retriever import VectorRetriever
from retrieval.graph_retriever import GraphRetriever
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.ranker import rank_contexts


class TestVectorRetriever:
    @patch('retrieval.vector_retriever.VectorRetriever._load_texts', return_value=["chunk1", "chunk2"])
    @patch('faiss.read_index')
    @patch('sentence_transformers.SentenceTransformer')
    def test_retrieve(self, mock_model_class, mock_read_index, mock_load_texts):
        # Mock the model
        mock_model = Mock()
        mock_model.encode.return_value = [[0.1, 0.2]]
        mock_model_class.return_value = mock_model

        # Mock the index
        mock_index = Mock()
        mock_index.search.return_value = ([[0.9, 0.8]], [[0, 1]])
        mock_read_index.return_value = mock_index

        retriever = VectorRetriever()
        results = retriever.retrieve("test query", top_k=2)

        assert len(results) == 2
        assert results[0]["source"] == "vector"
        assert results[0]["content"] == "chunk1"
        assert results[0]["score"] == 0.9


class TestGraphRetriever:
    def test_retrieve(self):
        mock_graph = Mock()
        mock_graph.run.return_value = [
            {"name": "Entity1", "type": "Person", "description": "A person"}
        ]

        retriever = GraphRetriever(graph_client=mock_graph)
        results = retriever.retrieve("test", entities=["TestEntity"])

        assert len(results) == 1
        assert results[0]["source"] == "graph"
        assert results[0]["related"] == "Entity1"


class TestRanker:
    def test_rank_contexts(self):
        vector_results = [{"content": "vector content", "score": 0.9}]
        graph_results = [{"entity": "A", "related": "B", "type": "Relation"}]

        ranked = rank_contexts(vector_results, graph_results)

        assert len(ranked) == 2
        # Vector results should have higher weight by default
        assert ranked[0]["weight"] == 0.7
        assert ranked[1]["weight"] == 0.3


class TestHybridRetriever:
    @patch('retrieval.hybrid_retriever.extract_entities', return_value=[{"name": "Entity1"}])
    def test_retrieve(self, mock_extract):
        # Create retriever with mocked components
        mock_vector = Mock()
        mock_vector.retrieve.return_value = [{"content": "vector result", "score": 0.9}]

        mock_graph = Mock()
        mock_graph.retrieve.return_value = [{"entity": "A", "related": "B", "type": "Relation"}]

        retriever = HybridRetriever(
            vector_retriever=mock_vector,
            graph_retriever=mock_graph
        )
        results = retriever.retrieve("test query")

        assert len(results) == 2
        mock_vector.retrieve.assert_called_once_with("test query", top_k=5)
        mock_graph.retrieve.assert_called_once()