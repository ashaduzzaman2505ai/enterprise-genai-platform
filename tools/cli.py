"""Small CLI to run ingestion, chunking, and graph building tasks.

Usage:
    python -m tools.cli ingest
    python -m tools.cli chunk
    python -m tools.cli graph
"""
import sys
from typing import Sequence


def _usage():
    print("Usage: python -m tools.cli [ingest|chunk|graph]")


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
    else:
        _usage()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
