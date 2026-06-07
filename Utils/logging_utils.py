import logging
import os
from datetime import datetime


class LoggingUtils:
    """Utility class for setting up logging configuration"""

    @staticmethod
    def setup_logger(log_filename):
        """
        Set up logger with file and console handlers

        Args:
            log_filename (str): Name of the log file

        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        # Full path for log file
        log_file_path = os.path.join(log_dir, log_filename)

        # Create logger
        logger = logging.getLogger(log_filename)
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        if logger.hasHandlers():
            logger.handlers.clear()

        # File handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
