"""Token tracking utilities for monitoring LLM usage and costs."""

import re
from typing import Dict, List, Optional, Any
from collections import defaultdict
import tiktoken

from common.logger import logger


class TokenTracker:
    """Tracks token usage across different operations and models."""

    def __init__(self):
        self.usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.encoders: Dict[str, Any] = {}

    def _get_encoder(self, model: str) -> Any:
        """Get or create a tiktoken encoder for the model.

        Args:
            model: Model name

        Returns:
            tiktoken encoder
        """
        if model not in self.encoders:
            try:
                # Map common model names to tiktoken encodings
                encoding_map = {
                    "gpt-4": "cl100k_base",
                    "gpt-4o": "cl100k_base",
                    "gpt-4o-mini": "cl100k_base",
                    "gpt-3.5-turbo": "cl100k_base",
                    "text-embedding-ada-002": "cl100k_base",
                    "text-davinci-003": "p50k_base",
                    "text-curie-001": "p50k_base",
                    "text-babbage-001": "p50k_base",
                    "text-ada-001": "p50k_base",
                }

                encoding = encoding_map.get(model, "cl100k_base")  # Default to GPT-4 encoding
                self.encoders[model] = tiktoken.get_encoding(encoding)
                logger.debug(f"Created encoder for model: {model} (encoding: {encoding})")

            except Exception as e:
                logger.warning(f"Failed to create tiktoken encoder for {model}: {e}. Using fallback.")
                self.encoders[model] = None

        return self.encoders[model]

    def count_tokens(self, text: str, model: str = "gpt-4o-mini") -> int:
        """Count tokens in text for a specific model.

        Args:
            text: Text to count tokens for
            model: Model name for tokenization

        Returns:
            Number of tokens
        """
        if not text:
            return 0

        encoder = self._get_encoder(model)
        if encoder:
            try:
                return len(encoder.encode(text))
            except Exception as e:
                logger.warning(f"Failed to encode text with tiktoken: {e}. Using fallback.")

        # Fallback: rough estimation
        return estimate_tokens(text)

    def track_usage(self, operation: str, model: str, prompt_tokens: int, completion_tokens: int) -> None:
        """Track token usage for an operation.

        Args:
            operation: Name of the operation
            model: Model used
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
        """
        self.usage[operation][f"{model}_prompt"] += prompt_tokens
        self.usage[operation][f"{model}_completion"] += completion_tokens
        self.usage[operation][f"{model}_total"] += prompt_tokens + completion_tokens

        logger.debug(f"Tracked usage for {operation}: {prompt_tokens} prompt + {completion_tokens} completion tokens")

    def get_usage_stats(self, operation: str) -> Dict[str, int]:
        """Get usage statistics for an operation.

        Args:
            operation: Name of the operation

        Returns:
            Dictionary with usage statistics
        """
        return dict(self.usage.get(operation, {}))

    def get_all_usage_stats(self) -> Dict[str, Dict[str, int]]:
        """Get usage statistics for all operations.

        Returns:
            Dictionary mapping operations to their usage stats
        """
        return {op: dict(stats) for op, stats in self.usage.items()}

    def estimate_cost(self, operation: str, model: str) -> float:
        """Estimate cost for an operation (USD).

        Args:
            operation: Name of the operation
            model: Model used

        Returns:
            Estimated cost in USD
        """
        stats = self.get_usage_stats(operation)

        # Cost per 1K tokens (approximate rates as of 2024)
        cost_map = {
            "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
            "gpt-4o": {"prompt": 0.005, "completion": 0.015},
            "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
        }

        costs = cost_map.get(model, {"prompt": 0.001, "completion": 0.002})  # Default rates

        prompt_tokens = stats.get(f"{model}_prompt", 0)
        completion_tokens = stats.get(f"{model}_completion", 0)

        cost = (prompt_tokens * costs["prompt"] + completion_tokens * costs["completion"]) / 1000
        return cost

    def reset(self) -> None:
        """Reset all usage tracking."""
        self.usage.clear()
        logger.info("Token tracker reset")


# Global tracker instance
_global_token_tracker = TokenTracker()


def estimate_tokens(text: str) -> int:
    """Estimate token count using a simple heuristic.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated number of tokens
    """
    if not text:
        return 0

    # Rough estimation: ~4 characters per token for English text
    # Adjust for punctuation and spaces
    words = re.findall(r'\b\w+\b', text)
    punctuation = len(re.findall(r'[.!?]', text))

    # Base estimation
    estimated = len(text) / 4

    # Adjust for word boundaries and punctuation
    estimated += len(words) * 0.1
    estimated += punctuation * 0.5

    return int(estimated)


def track_tokens(operation: str, model: str = "gpt-4o-mini"):
    """Decorator to track token usage for LLM calls.

    Args:
        operation: Name of the operation
        model: Model being used
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This is a simplified version - in practice, you'd need to intercept
            # the actual API calls to get accurate token counts
            result = func(*args, **kwargs)

            # Placeholder: estimate based on input/output if available
            if hasattr(result, '__len__') and isinstance(result, str):
                tokens = _global_token_tracker.count_tokens(result, model)
                _global_token_tracker.track_usage(operation, model, 0, tokens)  # Assume completion only

            return result
        return wrapper
    return decorator


def get_global_token_tracker() -> TokenTracker:
    """Get the global token tracker instance."""
    return _global_token_tracker
