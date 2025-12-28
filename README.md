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

