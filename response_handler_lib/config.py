import logging


class Config:
    ENABLE_LOGS = True
    LOGGER = logging.getLogger("response_handler_lib")


def configure_logger(logger):
    """Configure the logger to use."""
    Config.LOGGER = logger


def enable_logs(enable: bool):
    """Enable or disable logging."""
    Config.ENABLE_LOGS = enable
