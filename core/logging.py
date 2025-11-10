# core/logging.py
"""
Logging Configuration Module

Purpose:
- Centralizes and standardizes the application’s logging setup.
- Uses the `loguru` library for flexible, modern, and lightweight logging.
- Configures log levels and output format dynamically based on environment settings.

Usage:
    from core.logging import setup_logging
    logger = setup_logging()
    logger.info("Application started successfully.")
"""

from loguru import logger
from core.config import get_settings


def setup_logging():
    """
    Configure and return a pre-initialized `loguru` logger instance.

    Steps:
        1) Load logging level and configuration from environment settings.
        2) Remove any default log handlers.
        3) Add a simple stdout printer for clean console logging.

    Returns:
        logger (loguru.Logger): Configured logger instance ready for use.
    """
    settings = get_settings()

    # Remove any existing handlers to prevent duplicate log entries
    logger.remove()

    # Stream logs directly to stdout with the specified log level
    logger.add(lambda msg: print(msg, end=""), level=settings.LOG_LEVEL)

    return logger
