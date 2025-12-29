from typing import Optional

from retrieval.hybrid_retriever import HybridRetriever
from generation.reasoner import ReasoningEngine
from common.logger import logger


class AnswerGenerator:
    """Main class for generating answers to user queries using retrieval and reasoning."""

    def __init__(self, retriever: Optional[HybridRetriever] = None, reasoner: Optional[ReasoningEngine] = None):
        self.retriever = retriever or HybridRetriever()
        self.reasoner = reasoner or ReasoningEngine()
        logger.info("AnswerGenerator initialized")

    def answer(self, question: str) -> str:
        """Generate an answer for the given question.

        Args:
            question: The user's question.

        Returns:
            The generated answer.
        """
        logger.info(f"Generating answer for question: {question}")
        try:
            ranked_context = self.retriever.retrieve(question)
            logger.debug(f"Retrieved {len(ranked_context)} context items")
            answer = self.reasoner.reason(question, ranked_context)
            logger.info("Answer generated successfully")
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
