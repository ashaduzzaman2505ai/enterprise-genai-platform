from typing import List, Dict, Any

from generation.prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from generation.context_builder import build_context
from generation.llm_client import LLMClient
from common.logger import logger


class ReasoningEngine:
    """Engine for reasoning over retrieved context to generate answers."""

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()
        logger.info("ReasoningEngine initialized")

    def reason(self, question: str, ranked_context: List[Dict[str, Any]]) -> str:
        """Perform reasoning to generate an answer.

        Args:
            question: The user's question.
            ranked_context: List of retrieved context items.

        Returns:
            The reasoned answer.
        """
        logger.debug(f"Reasoning for question: {question}")
        try:
            context = build_context(ranked_context)
            logger.debug(f"Built context with {len(context)} characters")

            prompt = USER_PROMPT_TEMPLATE.format(
                question=question,
                context=context
            )

            answer = self.llm.generate(SYSTEM_PROMPT, prompt)
            logger.debug("LLM generation completed")
            return answer
        except Exception as e:
            logger.error(f"Error in reasoning: {e}")
            raise
