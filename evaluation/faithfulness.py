"""Faithfulness evaluation for checking if answers are supported by context."""

from typing import List, Dict, Any
import re
from difflib import SequenceMatcher

from common.logger import logger


def check_faithfulness(answer: str, context_blocks: List[str]) -> Dict[str, Any]:
    """Check if the answer is faithful to the provided context.

    Args:
        answer: Generated answer text
        context_blocks: List of context strings

    Returns:
        Dictionary with faithfulness assessment
    """
    if not answer.strip():
        return {
            "faithful": False,
            "unsupported_claims": ["Empty answer"],
            "score": 0.0
        }

    if not context_blocks:
        return {
            "faithful": False,
            "unsupported_claims": ["No context provided"],
            "score": 0.0
        }

    # Split answer into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', answer) if s.strip()]

    unsupported_claims = []
    supported_sentences = 0

    for sentence in sentences:
        if not _is_supported_by_context(sentence, context_blocks):
            unsupported_claims.append(sentence)
        else:
            supported_sentences += 1

    faithful = len(unsupported_claims) == 0
    score = supported_sentences / len(sentences) if sentences else 0.0

    logger.debug(f"Faithfulness check: {supported_sentences}/{len(sentences)} sentences supported")

    return {
        "faithful": faithful,
        "unsupported_claims": unsupported_claims,
        "score": score,
        "total_sentences": len(sentences),
        "supported_sentences": supported_sentences
    }


def _is_supported_by_context(sentence: str, context_blocks: List[str]) -> bool:
    """Check if a sentence is supported by any context block.

    Uses multiple strategies:
    1. Exact substring match
    2. High similarity match (>0.8)
    3. Key phrase overlap
    """
    sentence_lower = sentence.lower()

    for context in context_blocks:
        context_lower = context.lower()

        # Exact substring match
        if sentence_lower in context_lower:
            return True

        # High similarity match
        if SequenceMatcher(None, sentence_lower, context_lower).ratio() > 0.8:
            return True

        # Key phrase overlap (3+ word sequences)
        sentence_words = sentence_lower.split()
        context_words = context_lower.split()

        if len(sentence_words) >= 3:
            for i in range(len(sentence_words) - 2):
                phrase = ' '.join(sentence_words[i:i+3])
                if phrase in context_lower:
                    return True

    return False
