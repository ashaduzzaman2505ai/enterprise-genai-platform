import pytest
from unittest.mock import Mock, patch

from generation.answer_generator import AnswerGenerator
from generation.reasoner import ReasoningEngine
from generation.llm_client import LLMClient
from generation.context_builder import build_context


class TestLLMClient:
    @patch('generation.llm_client.OpenAI')
    def test_generate(self, mock_openai_class):
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test answer"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = LLMClient(api_key="test_key")
        result = client.generate("system", "user")

        assert result == "Test answer"
        mock_client.chat.completions.create.assert_called_once()


class TestContextBuilder:
    def test_build_context(self):
        chunks = [
            {"content": "First chunk"},
            {"content": "Second chunk"},
        ]
        context = build_context(chunks, max_chars=50)
        assert "First chunk" in context
        assert "Second chunk" in context


class TestReasoningEngine:
    @patch('generation.reasoner.LLMClient')
    @patch('generation.reasoner.build_context')
    def test_reason(self, mock_build_context, mock_llm_class):
        mock_llm = Mock()
        mock_llm.generate.return_value = "Reasoned answer"
        mock_llm_class.return_value = mock_llm

        mock_build_context.return_value = "Built context"

        engine = ReasoningEngine()
        result = engine.reason("test question", [{"content": "chunk"}])

        assert result == "Reasoned answer"
        mock_build_context.assert_called_once_with([{"content": "chunk"}])


class TestAnswerGenerator:
    @patch('generation.answer_generator.HybridRetriever')
    @patch('generation.answer_generator.ReasoningEngine')
    def test_answer(self, mock_reasoner_class, mock_retriever_class):
        mock_retriever = Mock()
        mock_retriever.retrieve.return_value = [{"content": "retrieved"}]
        mock_retriever_class.return_value = mock_retriever

        mock_reasoner = Mock()
        mock_reasoner.reason.return_value = "Final answer"
        mock_reasoner_class.return_value = mock_reasoner

        generator = AnswerGenerator()
        result = generator.answer("test question")

        assert result == "Final answer"
        mock_retriever.retrieve.assert_called_once_with("test question")
        mock_reasoner.reason.assert_called_once_with("test question", [{"content": "retrieved"}])