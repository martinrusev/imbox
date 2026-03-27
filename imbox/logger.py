"""Logger configuration for condense project.

Provides centralized logging setup for stdout.
"""

import logging

from .settings import settings


def setup_logger(name: str = "imbox") -> logging.Logger:
    """Set up a logger with console handle.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Set log level from settings
    log_level = getattr(logging, settings.log_level, logging.INFO)
    logger.setLevel(log_level)

    # Create formatter - structured for Kubernetes log aggregation
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "imbox") -> logging.Logger:
    """Get or create a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return setup_logger(name)
