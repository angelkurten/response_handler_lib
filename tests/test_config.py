import logging
import pytest
from response_handler_lib.config import Config, configure_logger, enable_logs, enable_context_in_json, enable_where_in_json

def test_configure_logger():
    # Create a test logger
    test_logger = logging.getLogger("test_logger")
    
    # Configure the logger
    configure_logger(test_logger)
    
    # Verify the logger was set
    assert Config.LOGGER == test_logger

def test_enable_logs():
    # Test enabling logs
    enable_logs(True)
    assert Config.ENABLE_LOGS is True
    
    # Test disabling logs
    enable_logs(False)
    assert Config.ENABLE_LOGS is False

def test_enable_context_in_json():
    # Test enabling context in JSON
    enable_context_in_json(True)
    assert Config.ENABLE_CONTEXT_IN_JSON is True
    
    # Test disabling context in JSON
    enable_context_in_json(False)
    assert Config.ENABLE_CONTEXT_IN_JSON is False

def test_enable_where_in_json():
    # Test enabling where in JSON
    enable_where_in_json(True)
    assert Config.ENABLE_WHERE_IN_JSON is True
    
    # Test disabling where in JSON
    enable_where_in_json(False)
    assert Config.ENABLE_WHERE_IN_JSON is False

def test_default_config_values():
    # Reset to default values
    enable_logs(True)
    enable_context_in_json(False)
    enable_where_in_json(False)
    
    # Test default values
    assert isinstance(Config.LOGGER, logging.Logger)
    assert Config.ENABLE_LOGS is True
    assert Config.ENABLE_CONTEXT_IN_JSON is False
    assert Config.ENABLE_WHERE_IN_JSON is False 