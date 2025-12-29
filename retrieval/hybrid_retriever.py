from typing import List, Dict, Any, Optional

from retrieval.vector_retriever import VectorRetriever
from retrieval.graph_retriever import GraphRetriever
from retrieval.ranker import rank_contexts
from retrieval.base import BaseRetriever
from knowledge_graph.entity_extractor import extract_entities
from common.logger import logger


class HybridRetriever(BaseRetriever):
    """Combines vector and graph retrieval for comprehensive search."""

    def __init__(
        self,
        vector_retriever: Optional[VectorRetriever] = None,
        graph_retriever: Optional[GraphRetriever] = None
    ):
        self.vector = vector_retriever or VectorRetriever()
        self.graph = graph_retriever or GraphRetriever()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        vector_weight: float = 0.7,
        graph_weight: float = 0.3,
        graph_depth: int = 2,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Perform hybrid retrieval combining vector and graph search.

        Args:
            query: The search query.
            top_k: Number of results to return.
            vector_weight: Weight for vector results.
            graph_weight: Weight for graph results.
            graph_depth: Depth for graph traversal.
            **kwargs: Additional parameters.

        Returns:
            Ranked list of retrieved contexts.
        """
        try:
            # Step 1: Vector retrieval for semantic similarity
            vector_results = self.vector.retrieve(query, top_k=top_k)
            logger.debug(f"Vector retrieval returned {len(vector_results)} results")

            # Step 2: Extract entities from query for graph retrieval
            entities_data = extract_entities(query)
            entities = [e["name"] for e in entities_data]
            logger.debug(f"Extracted entities: {entities}")

            # Step 3: Graph retrieval for related entities
            graph_results = []
            if entities:
                graph_results = self.graph.retrieve(query, entities=entities, depth=graph_depth)
                logger.debug(f"Graph retrieval returned {len(graph_results)} results")

            # Step 4: Rank and merge results
            ranked_results = rank_contexts(
                vector_results,
                graph_results,
                vector_weight=vector_weight,
                graph_weight=graph_weight
            )

            # Return top-k results
            return ranked_results[:top_k]

        except Exception as e:
            logger.error(f"Error in hybrid retrieval: {e}")
            # Fallback to vector-only retrieval
            try:
                return self.vector.retrieve(query, top_k=top_k)
            except Exception as fallback_e:
                logger.error(f"Fallback retrieval also failed: {fallback_e}")
                return []
