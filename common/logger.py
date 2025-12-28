from typing import Optional
import sys

from loguru import logger as _logger


def configure_logger(level: str = "INFO", sink: Optional = None) -> None:
    """Configure and replace the global logger.

    Calling multiple times is safe; it will remove previous handlers.
    """
    _logger.remove()
    _logger.add(
        sink or sys.stdout,
        format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        level=level,
    )


# Configure default logger on import for convenience.
configure_logger()

# Expose a module-level `logger` variable for callers.
logger = _logger

__all__ = ["logger", "configure_logger"]
