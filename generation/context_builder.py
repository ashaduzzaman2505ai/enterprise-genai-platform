from typing import List, Dict, Any

from common.logger import logger

MAX_CONTEXT_CHARS = 4000


def build_context(ranked_chunks: List[Dict[str, Any]], max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Build a context string from ranked chunks.

    Args:
        ranked_chunks: List of context items with 'content' key.
        max_chars: Maximum characters for the context.

    Returns:
        The built context string.
    """
    logger.debug(f"Building context from {len(ranked_chunks)} chunks")
    context_blocks = []
    total_chars = 0

    for item in ranked_chunks:
        content = item.get("content", "")
        block = f"- {content}"
        if total_chars + len(block) > max_chars:
            logger.debug(f"Context limit reached at {total_chars} chars")
            break
        context_blocks.append(block)
        total_chars += len(block)

    context = "\n".join(context_blocks)
    logger.debug(f"Built context with {len(context)} characters")
    return context
