import logging

import colorlog
from flask.logging import default_handler


class LoggingConfig:
    def __init__(self, config):
        self.LOG_LEVEL = config.get('LOG_LEVEL')
        self.LOG_FORMAT = config.get('LOG_FORMAT')
        self.LOG_DATE_FORMAT = config.get('LOG_DATE_FORMAT')

    def get_formatter(self):
        formatter = colorlog.ColoredFormatter(
            self.LOG_FORMAT,
            datefmt=self.LOG_DATE_FORMAT,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        return formatter

    def get_handler(self):
        handler = default_handler
        handler.setFormatter(self.get_formatter())
        handler.setLevel(self.LOG_LEVEL)
        handler.setFormatter(self.get_formatter())
        return handler

    def configure(self, logger: logging.Logger):
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(self.get_handler())
        return logger

    def getLogger(self, logger_name: str):
        logger = logging.getLogger(logger_name)
        self.configure(logger)
        return logger
