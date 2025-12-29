from openai import OpenAI
import os

from common.logger import logger
from common.config import settings


class LLMClient:
    """Client for interacting with OpenAI LLM API."""

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        logger.info(f"LLMClient initialized with model: {model}")

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """Generate a response from the LLM.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.
            temperature: Sampling temperature.

        Returns:
            The generated response.
        """
        logger.debug("Generating LLM response")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            content = response.choices[0].message.content
            logger.debug("LLM response generated successfully")
            return content
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise
