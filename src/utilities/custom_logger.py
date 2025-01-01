import logging
import coloredlogs

class Logger:
    def __init__(self, name: str, log_level: str = 'DEBUG'):
        """
        Initialize the Logger instance.
        :param name: The name for the logger (usually the module or app name).
        :param log_level: The log level for the logger (default: 'DEBUG').
        """
        # Remove all existing handlers from the root logger to prevent standard logging output
        logging.getLogger().handlers = []  # This will disable standard logging

        # Create custom logger
        self.logger = logging.getLogger(name)
        self.set_log_level(log_level)
        
        # Add colored stream handler for console output
        self._add_colored_stream_handler()

    def set_log_level(self, log_level: str):
        """Set the log level for the logger."""
        level = getattr(logging, log_level.upper(), logging.DEBUG)
        self.logger.setLevel(level)

    def _add_colored_stream_handler(self):
        """Add a StreamHandler with colored output to the console."""
        # Install coloredlogs for console output
        coloredlogs.install(level=logging.DEBUG, logger=self.logger, fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
