"""Script to check and query the knowledge graph."""

from common.logger import logger
from knowledge_graph.queries import GraphQueries


def main():
    logger.info("Checking knowledge graph...")

    queries = GraphQueries()
    try:
        # Get basic stats
        stats = queries.get_graph_stats()
        logger.info("Graph Statistics:")
        logger.info("  Entities: {}", stats["entities"])
        logger.info("  Documents: {}", stats["documents"])
        logger.info("  Relationships: {}", stats["relationships"])
        logger.info("  Entity Types: {}", stats["entity_types"])

        if stats["entities"] > 0:
            # Show sample entities
            entities = queries.list_entities(limit=10)
            logger.info("Sample Entities:")
            for ent in entities:
                logger.info("  {} ({})", ent["name"], ent["type"])

            # Try to find related entities for the first entity
            if entities:
                first_entity = entities[0]["name"]
                related = queries.find_related_entities(first_entity, limit=5)
                if related:
                    logger.info("Entities related to '{}':", first_entity)
                    for rel in related:
                        logger.info("  {} ({}) - {}", rel["name"], rel["type"], rel["relation"])
                else:
                    logger.info("No related entities found for '{}'", first_entity)
        else:
            logger.warning("No entities found in graph")

    except Exception as e:
        logger.error("Failed to query graph: {}", e)
        raise
    finally:
        queries.close()


if __name__ == "__main__":
    main()