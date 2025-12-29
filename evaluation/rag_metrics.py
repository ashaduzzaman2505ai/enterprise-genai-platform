"""RAG evaluation metrics for measuring retrieval and generation quality."""

from typing import List, Dict, Any, Set
import re
from collections import Counter

from common.logger import logger


def context_recall(retrieved_chunks: List[Dict[str, Any]], gold_chunks: List[str]) -> float:
    """Calculate context recall: fraction of relevant chunks retrieved.

    Args:
        retrieved_chunks: List of retrieved chunk dictionaries with 'content' key
        gold_chunks: List of gold standard chunk contents

    Returns:
        Recall score between 0 and 1
    """
    if not gold_chunks:
        logger.warning("No gold chunks provided for recall calculation")
        return 0.0

    retrieved_content = {chunk.get("content", "") for chunk in retrieved_chunks}
    gold_content = set(gold_chunks)

    matching = len(retrieved_content & gold_content)
    recall = matching / len(gold_content)

    logger.debug(f"Context recall: {matching}/{len(gold_content)} = {recall:.3f}")
    return recall


def context_precision(retrieved_chunks: List[Dict[str, Any]], gold_chunks: List[str]) -> float:
    """Calculate context precision: fraction of retrieved chunks that are relevant.

    Args:
        retrieved_chunks: List of retrieved chunk dictionaries with 'content' key
        gold_chunks: List of gold standard chunk contents

    Returns:
        Precision score between 0 and 1
    """
    if not retrieved_chunks:
        logger.warning("No retrieved chunks for precision calculation")
        return 0.0

    retrieved_content = {chunk.get("content", "") for chunk in retrieved_chunks}
    gold_content = set(gold_chunks)

    matching = len(retrieved_content & gold_content)
    precision = matching / len(retrieved_chunks)

    logger.debug(f"Context precision: {matching}/{len(retrieved_chunks)} = {precision:.3f}")
    return precision


def answer_relevance(answer: str, question: str) -> float:
    """Calculate answer relevance using semantic similarity heuristics.

    Args:
        answer: Generated answer text
        question: Original question

    Returns:
        Relevance score between 0 and 1
    """
    if not answer or not question:
        return 0.0

    # Simple heuristic: overlap of important words
    question_words = set(re.findall(r'\b\w+\b', question.lower()))
    answer_words = set(re.findall(r'\b\w+\b', answer.lower()))

    # Remove stop words (basic list)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}

    question_words = question_words - stop_words
    answer_words = answer_words - stop_words

    if not question_words:
        return 0.0

    overlap = len(question_words & answer_words)
    relevance = overlap / len(question_words)

    logger.debug(f"Answer relevance: {overlap}/{len(question_words)} = {relevance:.3f}")
    return min(relevance, 1.0)  # Cap at 1.0


def calculate_f1(precision: float, recall: float) -> float:
    """Calculate F1 score from precision and recall.

    Args:
        precision: Precision score
        recall: Recall score

    Returns:
        F1 score
    """
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)
