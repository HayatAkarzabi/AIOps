# Simple logging utility for the AIOps platform.
# Wraps Python's logging module with a consistent format.

import logging
import sys

def setup_logger(name: str = "aiops", level: str = "INFO"):
    """
    Creates and returns a logger with a standard format.
    Usage:
        logger = setup_logger(__name__)
        logger.info("This is an info message")
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
