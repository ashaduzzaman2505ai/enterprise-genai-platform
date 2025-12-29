# Enterprise GenAI Platform

A comprehensive platform for enterprise generative AI applications with knowledge graph capabilities.

## Setup

### Prerequisites

- Python 3.12+
- Neo4j AuraDB Free (Cloud instance)

### Environment Configuration

1. Copy the environment variables from `.env` and update with your credentials:

```bash
# Required for Neo4j AuraDB
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Optional: OpenAI API for embeddings
OPENAI_API_KEY=your-openai-key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Neo4j AuraDB Setup

This platform uses Neo4j AuraDB Free for the knowledge graph. To set up:

1. Create a free account at [Neo4j Aura](https://neo4j.com/aura/)
2. Create a new database instance
3. Copy the connection URI (neo4j+s:// format) and credentials to your `.env` file
4. The platform will automatically connect to your AuraDB instance

### Usage

#### CLI Commands

The platform provides a comprehensive CLI for all operations:

```bash
# Data ingestion and processing
python -m tools.cli ingest          # Ingest documents from data/raw/
python -m tools.cli chunk           # Process documents into chunks

# Knowledge graph operations
python -m tools.cli graph           # Build knowledge graph
python -m tools.cli check           # Check graph status

# Retrieval and generation
python -m tools.cli retrieve "query"    # Retrieve relevant information
python -m tools.cli generate "question" # Generate answers to questions

# Evaluation and monitoring
python -m tools.cli evaluate        # Run comprehensive evaluation
python -m tools.cli monitor         # View performance metrics
python -m tools.cli test            # Run prompt regression tests
```

#### Direct Script Usage

Alternatively, you can run individual scripts:

Build the knowledge graph:
```bash
python scripts/build_graph.py
```

Check the graph status:
```bash
python scripts/check_graph.py
```

Index document chunks:
```bash
python scripts/index_chunks.py
```

