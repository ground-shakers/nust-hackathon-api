"""Configure and return a logger instance.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Configure and return a logger instance"""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                os.path.join(log_dir, "healthcare_api.log"),
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
            ),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("healthcare_api")


# Create a global logger instance
logger = setup_logger()