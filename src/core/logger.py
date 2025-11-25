import logging
import sys
from .config import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with the specified name and configuration.
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Default logger instance
logger = setup_logger("asset_mgmt_analytics")
