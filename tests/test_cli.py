"""Tests for CLI functionality."""

import pytest
from unittest.mock import patch, MagicMock
from tools.cli import main


class TestCLI:
    """Test CLI commands."""

    @patch('ingestion.run_ingestion.ingest')
    def test_ingest_command(self, mock_ingest):
        """Test ingest command."""
        result = main(['ingest'])
        assert result == 0
        mock_ingest.assert_called_once()

    @patch('chunking.run_chunking.run')
    def test_chunk_command(self, mock_run):
        """Test chunk command."""
        result = main(['chunk'])
        assert result == 0
        mock_run.assert_called_once()

    @patch('scripts.build_graph.main')
    def test_graph_command(self, mock_build_graph):
        """Test graph command."""
        result = main(['graph'])
        assert result == 0
        mock_build_graph.assert_called_once()

    @patch('scripts.check_graph.main')
    def test_check_command(self, mock_check_graph):
        """Test check command."""
        result = main(['check'])
        assert result == 0
        mock_check_graph.assert_called_once()

    @patch('retrieval.hybrid_retriever.HybridRetriever')
    def test_retrieve_command(self, mock_retriever_class):
        """Test retrieve command."""
        mock_retriever = MagicMock()
        mock_retriever.retrieve.return_value = [
            {'source': 'vector', 'content': 'test content 1'},
            {'source': 'graph', 'content': 'test content 2'}
        ]
        mock_retriever_class.return_value = mock_retriever

        result = main(['retrieve', 'test query'])
        assert result == 0
        mock_retriever.retrieve.assert_called_once_with('test query')

    def test_retrieve_command_no_query(self):
        """Test retrieve command without query."""
        result = main(['retrieve'])
        assert result == 2

    @patch('generation.answer_generator.AnswerGenerator')
    def test_generate_command(self, mock_generator_class):
        """Test generate command."""
        mock_generator = MagicMock()
        mock_generator.answer.return_value = 'Generated answer'
        mock_generator_class.return_value = mock_generator

        result = main(['generate', 'test question'])
        assert result == 0
        mock_generator.answer.assert_called_once_with('test question')

    def test_generate_command_no_question(self):
        """Test generate command without question."""
        result = main(['generate'])
        assert result == 2

    @patch('evaluation.run_evaluation.run_evaluation')
    def test_evaluate_command(self, mock_run_evaluation):
        """Test evaluate command."""
        mock_run_evaluation.return_value = {'summary': {'mean_recall': 0.8}}
        result = main(['evaluate'])
        assert result == 0
        mock_run_evaluation.assert_called_once()

    @patch('monitoring.latency_tracker.get_global_tracker')
    @patch('monitoring.token_tracker.get_global_token_tracker')
    def test_monitor_command(self, mock_token_tracker, mock_latency_tracker):
        """Test monitor command."""
        mock_latency = MagicMock()
        mock_latency.get_all_stats.return_value = {}
        mock_latency_tracker.return_value = mock_latency

        mock_token = MagicMock()
        mock_token.get_all_usage_stats.return_value = {}
        mock_token_tracker.return_value = mock_token

        result = main(['monitor'])
        assert result == 0
        mock_latency.get_all_stats.assert_called_once()
        mock_token.get_all_usage_stats.assert_called_once()

    def test_invalid_command(self):
        """Test invalid command."""
        result = main(['invalid'])
        assert result == 2

    @patch('ci.prompt_regression_test.PromptRegressionTester')
    def test_test_command(self, mock_tester_class):
        """Test test command."""
        mock_tester = MagicMock()
        mock_tester.run_regression_tests.return_value = {
            'passed_tests': 4,
            'total_tests': 5,
            'success_rate': 0.8
        }
        mock_tester_class.return_value = mock_tester

        result = main(['test'])
        assert result == 0
        mock_tester.run_regression_tests.assert_called_once()

    @patch('ci.prompt_regression_test.PromptRegressionTester')
    def test_test_command_failure(self, mock_tester_class):
        """Test test command with failure."""
        mock_tester = MagicMock()
        mock_tester.run_regression_tests.return_value = {
            'passed_tests': 1,
            'total_tests': 5,
            'success_rate': 0.2
        }
        mock_tester_class.return_value = mock_tester

        result = main(['test'])
        assert result == 1  # Should return 1 for low success rate


if __name__ == "__main__":
    pytest.main([__file__])