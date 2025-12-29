"""Prompt regression testing for CI/CD pipeline."""

import pytest
from typing import List, Dict, Any
import json
from pathlib import Path

from generation.answer_generator import AnswerGenerator
from common.logger import logger


class PromptRegressionTester:
    """Test for prompt regression by checking expected keywords in answers."""

    def __init__(self, generator: AnswerGenerator = None):
        self.generator = generator or AnswerGenerator()

    def test_question_answer_coverage(
        self,
        question: str,
        expected_keywords: List[str],
        min_coverage: float = 0.5
    ) -> Dict[str, Any]:
        """Test if an answer covers expected keywords.

        Args:
            question: Question to ask
            expected_keywords: Keywords that should appear in the answer
            min_coverage: Minimum coverage ratio required (0-1)

        Returns:
            Test result dictionary
        """
        logger.info(f"Testing question: {question}")

        try:
            answer = self.generator.answer(question)
            answer_lower = answer.lower()

            found_keywords = []
            missing_keywords = []

            for keyword in expected_keywords:
                if keyword.lower() in answer_lower:
                    found_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)

            coverage = len(found_keywords) / len(expected_keywords) if expected_keywords else 0
            passed = coverage >= min_coverage

            result = {
                "question": question,
                "answer": answer,
                "expected_keywords": expected_keywords,
                "found_keywords": found_keywords,
                "missing_keywords": missing_keywords,
                "coverage": coverage,
                "min_coverage": min_coverage,
                "passed": passed
            }

            status = "PASSED" if passed else "FAILED"
            logger.info(f"Test {status}: {coverage:.2f} coverage ({len(found_keywords)}/{len(expected_keywords)} keywords)")

            if not passed:
                logger.warning(f"Missing keywords: {missing_keywords}")

            return result

        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            return {
                "question": question,
                "error": str(e),
                "passed": False
            }

    def run_regression_tests(self, test_file: Path = None) -> Dict[str, Any]:
        """Run all regression tests from a test file.

        Args:
            test_file: Path to JSON file with test cases

        Returns:
            Summary of test results
        """
        if test_file is None:
            test_file = Path(__file__).parent.parent / "evaluation" / "test_cases.json"

        logger.info(f"Running regression tests from {test_file}")

        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load test cases: {e}")
            return {"error": str(e), "passed": False}

        results = []
        passed_count = 0

        for test_case in test_cases:
            question = test_case["question"]
            expected_keywords = test_case.get("expected_answer_keywords", [])

            result = self.test_question_answer_coverage(
                question=question,
                expected_keywords=expected_keywords
            )

            results.append(result)
            if result.get("passed", False):
                passed_count += 1

        summary = {
            "total_tests": len(results),
            "passed_tests": passed_count,
            "failed_tests": len(results) - passed_count,
            "success_rate": passed_count / len(results) if results else 0,
            "results": results
        }

        logger.info(f"Regression testing completed: {passed_count}/{len(results)} tests passed")

        return summary


# Global tester instance
_tester = PromptRegressionTester()


def test_basic_regression():
    """Basic regression test for CI."""
    result = _tester.test_question_answer_coverage(
        question="What are the main energy policies?",
        expected_keywords=["policy", "energy", "government"]
    )
    assert result["passed"], f"Test failed: {result}"


def test_comprehensive_regression():
    """Run comprehensive regression tests."""
    summary = _tester.run_regression_tests()
    success_rate = summary.get("success_rate", 0)

    # Require at least 60% success rate for CI to pass
    assert success_rate >= 0.6, f"Regression test success rate too low: {success_rate:.2f}"

    # Log detailed results
    logger.info(f"Regression test summary: {summary['passed_tests']}/{summary['total_tests']} passed")


if __name__ == "__main__":
    # Run tests manually
    print("Running prompt regression tests...")

    # Basic test
    result = _tester.test_question_answer_coverage(
        question="What fiscal incentives are provided to private power companies?",
        expected_keywords=["tax", "exemption", "corporate"]
    )

    print(f"Basic test result: {'PASSED' if result['passed'] else 'FAILED'}")
    print(f"Coverage: {result['coverage']:.2f}")

    # Comprehensive test
    summary = _tester.run_regression_tests()
    print(f"\nComprehensive test results: {summary['passed_tests']}/{summary['total_tests']} passed")
    print(".2f")



# Missing keywords: ['competitive bidding', 'lowest levelized tariff', 'participation', '20%', 'tax', 'exemption', 'corporate', 'income', 'customs', 'duty', 'vat']