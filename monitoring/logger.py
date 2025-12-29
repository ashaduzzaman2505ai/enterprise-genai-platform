"""Monitoring-specific logging utilities."""

import os
from pathlib import Path
from typing import Optional

from common.logger import logger, configure_logger


def setup_monitoring_logger(
    log_file: Optional[str] = None,
    level: str = "INFO",
    enable_file_logging: bool = True
) -> None:
    """Set up monitoring-specific logging configuration.

    Args:
        log_file: Path to log file (default: monitoring.log in data directory)
        level: Logging level
        enable_file_logging: Whether to enable file logging
    """
    # Get data directory
    from common.config import settings
    data_dir = settings.ensure_data_dir()

    if log_file is None:
        log_file = data_dir / "monitoring.log"

    # Configure main logger
    configure_logger(level=level)

    if enable_file_logging:
        # Add file handler for monitoring logs
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove any existing file handlers to avoid duplicates
        logger.remove()

        # Reconfigure with file logging
        logger.add(
            log_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level=level,
            rotation="10 MB",  # Rotate when file reaches 10MB
            retention="30 days",  # Keep logs for 30 days
            encoding="utf-8"
        )

        # Also log to console
        logger.add(
            os.sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level=level,
            colorize=True
        )

        logger.info(f"Monitoring logging configured. Log file: {log_path}")


def log_performance_metrics(operation: str, latency: float, token_count: Optional[int] = None, **kwargs) -> None:
    """Log performance metrics in a structured way.

    Args:
        operation: Name of the operation
        latency: Latency in seconds
        token_count: Number of tokens used (optional)
        **kwargs: Additional metrics to log
    """
    metrics = {
        "operation": operation,
        "latency_seconds": latency,
        "tokens": token_count,
        **kwargs
    }

    # Filter out None values
    metrics = {k: v for k, v in metrics.items() if v is not None}

    logger.info("PERFORMANCE_METRICS", extra=metrics)


def log_error_with_context(error: Exception, operation: str, **context) -> None:
    """Log an error with additional context information.

    Args:
        error: The exception that occurred
        operation: Name of the operation where error occurred
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    logger.error(f"Error in {operation}: {error} | Context: {context_str}")


# Initialize monitoring logger on import
setup_monitoring_logger()