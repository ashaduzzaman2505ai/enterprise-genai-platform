from typing import List, Dict, Any
from common.logger import logger


def rank_contexts(
    vector_results: List[Dict[str, Any]],
    graph_results: List[Dict[str, Any]],
    vector_weight: float = 0.7,
    graph_weight: float = 0.3
) -> List[Dict[str, Any]]:
    """Rank and merge results from vector and graph retrieval.

    Args:
        vector_results: Results from vector retriever.
        graph_results: Results from graph retriever.
        vector_weight: Weight for vector results (0-1).
        graph_weight: Weight for graph results (0-1).

    Returns:
        Ranked list of contexts with weights.
    """
    if not (0 <= vector_weight <= 1 and 0 <= graph_weight <= 1):
        logger.warning("Weights should be between 0 and 1, using defaults")
        vector_weight = 0.7
        graph_weight = 0.3

    ranked = []

    # Add vector results with semantic relevance weight
    for result in vector_results:
        ranked.append({
            "weight": vector_weight,
            "content": result.get("content", ""),
            "source": "vector",
            "score": result.get("score", 0.0),
            "metadata": result
        })

    # Add graph results with reasoning relevance weight
    for result in graph_results:
        content = result.get("description", "")
        if not content:
            content = f"{result.get('entity', '')} is related to {result.get('related', '')} ({result.get('type', '')})"

        ranked.append({
            "weight": graph_weight,
            "content": content,
            "source": "graph",
            "metadata": result
        })

    # Sort by weight descending, then by score if available
    ranked.sort(key=lambda x: (x["weight"], x.get("score", 0)), reverse=True)

    logger.debug(f"Ranked {len(ranked)} contexts")
    return ranked
