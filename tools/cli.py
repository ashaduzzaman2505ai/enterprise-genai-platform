"""Small CLI to run ingestion, chunking, graph building, checking, and retrieval tasks.

Usage:
    python -m tools.cli ingest
    python -m tools.cli chunk
    python -m tools.cli graph
    python -m tools.cli check
    python -m tools.cli retrieve <query>
"""
import sys
from typing import Sequence


def _usage():
    print("Usage: python -m tools.cli [ingest|chunk|graph|check|retrieve] [query]")


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if not argv:
        _usage()
        return 2

    cmd = argv[0]

    if cmd == "ingest":
        from ingestion.run_ingestion import ingest

        ingest()
        return 0
    elif cmd == "chunk":
        from chunking.run_chunking import run

        run()
        return 0
    elif cmd == "graph":
        from scripts.build_graph import main as build_graph

        build_graph()
        return 0
    elif cmd == "check":
        from scripts.check_graph import main as check_graph

        check_graph()
        return 0
    elif cmd == "retrieve":
        if len(argv) < 2:
            print("Error: retrieve command requires a query")
            _usage()
            return 2

        query = " ".join(argv[1:])
        from retrieval.hybrid_retriever import HybridRetriever

        retriever = HybridRetriever()
        results = retriever.retrieve(query)

        print(f"Retrieved {len(results)} results for query: '{query}'")
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['source']}] {result['content'][:100]}...")
        return 0
    else:
        _usage()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
