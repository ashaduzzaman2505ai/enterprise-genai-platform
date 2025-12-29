"""Small CLI to run ingestion, chunking, graph building, checking, retrieval, generation, evaluation, monitoring, and testing tasks.

Usage:
    python -m tools.cli ingest
    python -m tools.cli chunk
    python -m tools.cli graph
    python -m tools.cli check
    python -m tools.cli retrieve <query>
    python -m tools.cli generate <question>
    python -m tools.cli evaluate
    python -m tools.cli monitor
    python -m tools.cli test
"""
import sys
from typing import Sequence


def _usage():
    print("Usage: python -m tools.cli [ingest|chunk|graph|check|retrieve|generate|evaluate|monitor|test] [args]")


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
    elif cmd == "generate":
        if len(argv) < 2:
            print("Error: generate command requires a question")
            _usage()
            return 2

        question = " ".join(argv[1:])
        from generation.answer_generator import AnswerGenerator

        generator = AnswerGenerator()
        answer = generator.answer(question)

        print(f"Question: {question}")
        print(f"Answer: {answer}")
        return 0
    elif cmd == "evaluate":
        from evaluation.run_evaluation import run_evaluation

        results = run_evaluation()
        return 0
    elif cmd == "monitor":
        from monitoring.latency_tracker import get_global_tracker
        from monitoring.token_tracker import get_global_token_tracker

        latency_tracker = get_global_tracker()
        token_tracker = get_global_token_tracker()

        print("=== LATENCY STATISTICS ===")
        latency_stats = latency_tracker.get_all_stats()
        if latency_stats:
            for op, stats in latency_stats.items():
                print(f"{op}: {stats['count']} calls, avg {stats['mean']:.3f}s")
        else:
            print("No latency data recorded")

        print("\n=== TOKEN USAGE STATISTICS ===")
        token_stats = token_tracker.get_all_usage_stats()
        if token_stats:
            for op, stats in token_stats.items():
                total_tokens = stats.get(f"gpt-4o-mini_total", 0)
                print(f"{op}: {total_tokens} total tokens")
        else:
            print("No token usage data recorded")

        return 0
    elif cmd == "test":
        from ci.prompt_regression_test import PromptRegressionTester

        tester = PromptRegressionTester()
        summary = tester.run_regression_tests()

        print(f"Prompt regression test results: {summary['passed_tests']}/{summary['total_tests']} passed")
        print(".2f")

        # Return non-zero if tests failed
        if summary.get('success_rate', 0) < 0.6:  # Require 60% pass rate
            return 1
        return 0
    else:
        _usage()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
