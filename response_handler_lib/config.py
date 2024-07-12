import logging


class Config:
    ENABLE_LOGS = True
    LOGGER = logging.getLogger("response_handler_lib")
    ENABLE_CONTEXT_IN_JSON = False
    ENABLE_WHERE_IN_JSON = False


def configure_logger(logger):
    """Configure the logger to use."""
    Config.LOGGER = logger


def enable_logs(enable: bool):
    """Enable or disable logging."""
    Config.ENABLE_LOGS = enable


def enable_context_in_json(enable: bool):
    """Enable or disable context information in the JSON response"""
    Config.ENABLE_CONTEXT_IN_JSON = enable


def enable_where_in_json(enable: bool):
    """Enable or disable error location information in the JSON response."""
    Config.ENABLE_WHERE_IN_JSON = enable
