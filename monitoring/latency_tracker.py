"""Latency tracking utilities for monitoring system performance."""

import time
from functools import wraps
from typing import Dict, List, Optional, Callable, Any
from collections import defaultdict
import statistics

from common.logger import logger


class LatencyTracker:
    """Tracks latency metrics for operations."""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.current_operations: Dict[str, float] = {}

    def start_operation(self, operation_name: str) -> None:
        """Start timing an operation.

        Args:
            operation_name: Name of the operation to track
        """
        self.current_operations[operation_name] = time.time()
        logger.debug(f"Started timing operation: {operation_name}")

    def end_operation(self, operation_name: str) -> float:
        """End timing an operation and record the latency.

        Args:
            operation_name: Name of the operation

        Returns:
            Latency in seconds
        """
        if operation_name not in self.current_operations:
            logger.warning(f"Operation '{operation_name}' was not started")
            return 0.0

        start_time = self.current_operations.pop(operation_name)
        latency = time.time() - start_time
        self.metrics[operation_name].append(latency)

        logger.debug(f"Operation '{operation_name}' completed in {latency:.3f}s")
        return latency

    def get_stats(self, operation_name: str) -> Dict[str, float]:
        """Get statistics for an operation.

        Args:
            operation_name: Name of the operation

        Returns:
            Dictionary with latency statistics
        """
        latencies = self.metrics.get(operation_name, [])
        if not latencies:
            return {"count": 0, "mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0}

        return {
            "count": len(latencies),
            "mean": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "min": min(latencies),
            "max": max(latencies)
        }

    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all operations.

        Returns:
            Dictionary mapping operation names to their statistics
        """
        return {op: self.get_stats(op) for op in self.metrics.keys()}

    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.current_operations.clear()
        logger.info("Latency tracker reset")


# Global tracker instance
_global_tracker = LatencyTracker()


def track_latency(operation_name: Optional[str] = None):
    """Decorator to track latency of a function.

    Args:
        operation_name: Optional name for the operation (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            op_name = operation_name or f"{func.__module__}.{func.__qualname__}"
            _global_tracker.start_operation(op_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                latency = _global_tracker.end_operation(op_name)
                logger.info(f"[LATENCY] {op_name}: {latency:.3f}s")

        return wrapper
    return decorator


def get_global_tracker() -> LatencyTracker:
    """Get the global latency tracker instance."""
    return _global_tracker


# Convenience functions for global tracker
def start_timing(operation_name: str) -> None:
    """Start timing a global operation."""
    _global_tracker.start_operation(operation_name)


def end_timing(operation_name: str) -> float:
    """End timing a global operation."""
    return _global_tracker.end_operation(operation_name)


def get_latency_stats(operation_name: str) -> Dict[str, float]:
    """Get latency statistics for a global operation."""
    return _global_tracker.get_stats(operation_name)
