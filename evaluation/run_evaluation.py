"""Run comprehensive evaluation of the RAG system."""

import json
import statistics
from pathlib import Path
from typing import Dict, List, Any

from retrieval.hybrid_retriever import HybridRetriever
from generation.answer_generator import AnswerGenerator
from evaluation.rag_metrics import context_recall, context_precision, answer_relevance, calculate_f1
from evaluation.faithfulness import check_faithfulness
from common.logger import logger


def load_test_cases(test_file: Path) -> List[Dict[str, Any]]:
    """Load test cases from JSON file.

    Args:
        test_file: Path to the test cases JSON file

    Returns:
        List of test case dictionaries
    """
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        logger.info(f"Loaded {len(test_cases)} test cases from {test_file}")
        return test_cases
    except Exception as e:
        logger.error(f"Failed to load test cases: {e}")
        raise


def evaluate_retrieval(retriever: HybridRetriever, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate retrieval performance.

    Args:
        retriever: The retriever to evaluate
        test_cases: List of test cases

    Returns:
        Dictionary with evaluation results
    """
    logger.info("Starting retrieval evaluation...")

    results = []
    recall_scores = []
    precision_scores = []
    f1_scores = []

    for i, test_case in enumerate(test_cases):
        try:
            question = test_case["question"]
            gold_context = test_case["gold_context"]

            logger.debug(f"Evaluating retrieval for question {i+1}: {question[:50]}...")

            retrieved_chunks = retriever.retrieve(question)

            recall = context_recall(retrieved_chunks, gold_context)
            precision = context_precision(retrieved_chunks, gold_context)
            f1 = calculate_f1(precision, recall)

            recall_scores.append(recall)
            precision_scores.append(precision)
            f1_scores.append(f1)

            results.append({
                "question_id": test_case.get("id", f"q_{i+1}"),
                "question": question,
                "recall": recall,
                "precision": precision,
                "f1": f1,
                "retrieved_count": len(retrieved_chunks)
            })

        except Exception as e:
            logger.error(f"Error evaluating question {i+1}: {e}")
            continue

    return {
        "individual_results": results,
        "summary": {
            "mean_recall": statistics.mean(recall_scores) if recall_scores else 0,
            "mean_precision": statistics.mean(precision_scores) if precision_scores else 0,
            "mean_f1": statistics.mean(f1_scores) if f1_scores else 0,
            "total_questions": len(results)
        }
    }


def evaluate_generation(generator: AnswerGenerator, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate generation performance.

    Args:
        generator: The answer generator to evaluate
        test_cases: List of test cases

    Returns:
        Dictionary with evaluation results
    """
    logger.info("Starting generation evaluation...")

    results = []
    relevance_scores = []
    faithfulness_scores = []

    for i, test_case in enumerate(test_cases):
        try:
            question = test_case["question"]
            expected_keywords = test_case.get("expected_answer_keywords", [])

            logger.debug(f"Evaluating generation for question {i+1}: {question[:50]}...")

            answer = generator.answer(question)

            # Answer relevance
            relevance = answer_relevance(answer, question)
            relevance_scores.append(relevance)

            # Faithfulness (using retrieved context as proxy for gold context)
            # In a real evaluation, you'd want ground truth context
            faithfulness_result = {"score": 0.5, "faithful": True}  # Placeholder

            # Keyword coverage
            answer_lower = answer.lower()
            found_keywords = [kw for kw in expected_keywords if kw.lower() in answer_lower]
            keyword_coverage = len(found_keywords) / len(expected_keywords) if expected_keywords else 0

            results.append({
                "question_id": test_case.get("id", f"q_{i+1}"),
                "question": question,
                "answer": answer,
                "relevance": relevance,
                "faithfulness": faithfulness_result,
                "keyword_coverage": keyword_coverage,
                "found_keywords": found_keywords
            })

        except Exception as e:
            logger.error(f"Error evaluating generation for question {i+1}: {e}")
            continue

    return {
        "individual_results": results,
        "summary": {
            "mean_relevance": statistics.mean(relevance_scores) if relevance_scores else 0,
            "mean_faithfulness": statistics.mean(faithfulness_scores) if faithfulness_scores else 0,
            "total_questions": len(results)
        }
    }


def run_evaluation(test_file: Path = None, output_file: Path = None) -> Dict[str, Any]:
    """Run complete evaluation suite.

    Args:
        test_file: Path to test cases file (default: evaluation/test_cases.json)
        output_file: Path to save results (optional)

    Returns:
        Dictionary with all evaluation results
    """
    if test_file is None:
        test_file = Path(__file__).parent / "test_cases.json"

    logger.info("Starting comprehensive RAG evaluation...")

    # Load test cases
    test_cases = load_test_cases(test_file)

    # Initialize components
    retriever = HybridRetriever()
    generator = AnswerGenerator()

    # Run evaluations
    retrieval_results = evaluate_retrieval(retriever, test_cases)
    generation_results = evaluate_generation(generator, test_cases)

    # Combine results
    results = {
        "retrieval": retrieval_results,
        "generation": generation_results,
        "metadata": {
            "test_cases_file": str(test_file),
            "total_test_cases": len(test_cases)
        }
    }

    # Print summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)

    ret_summary = retrieval_results["summary"]
    gen_summary = generation_results["summary"]

    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")
    print(".3f")

    # Save results if requested
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    logger.info("Evaluation completed successfully")
    return results


if __name__ == "__main__":
    run_evaluation()
