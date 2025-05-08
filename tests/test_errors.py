import pytest
from response_handler_lib.errors import ErrorResponse, ErrorResponseConfig
from response_handler_lib.error_codes import ERROR_MESSAGES


def test_error_response_creation():
    # Test basic error response creation
    error = ErrorResponse(code="TEST_ERROR", message="Test error message")
    assert error.code == "TEST_ERROR"
    assert error.message == "Test error message"
    assert error.where is None

    # Test error response with where field
    error = ErrorResponse(
        code="TEST_ERROR",
        message="Test error message",
        where="In test function"
    )
    assert error.code == "TEST_ERROR"
    assert error.message == "Test error message"
    assert error.where == "In test function"


def test_error_response_config_custom_error():
    # Test adding a single custom error
    ErrorResponseConfig.add_custom_error("CUSTOM_ERROR", "Custom error message")
    error = ErrorResponseConfig.get_error("CUSTOM_ERROR")
    assert error is not None
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "Custom error message"

    # Test adding a custom error that overwrites an existing one
    ErrorResponseConfig.add_custom_error("VAL_ERROR", "Custom validation error")
    error = ErrorResponseConfig.get_error("VAL_ERROR")
    assert error is not None
    assert error.code == "VAL_ERROR"
    assert error.message == "Custom validation error"


def test_error_response_config_custom_errors():
    # Test adding multiple custom errors
    custom_errors = {
        "ERROR_1": "First custom error",
        "ERROR_2": "Second custom error",
        "ERROR_3": "Third custom error"
    }
    ErrorResponseConfig.add_custom_errors(custom_errors)

    # Verify all errors were added
    for code, message in custom_errors.items():
        error = ErrorResponseConfig.get_error(code)
        assert error is not None
        assert error.code == code
        assert error.message == message


def test_error_response_config_get_error():
    # Test getting an existing error
    error = ErrorResponseConfig.get_error("VAL_ERROR")
    assert error is not None
    assert error.code == "VAL_ERROR"
    assert error.message == ERROR_MESSAGES["VAL_ERROR"]

    # Test getting a non-existent error
    error = ErrorResponseConfig.get_error("NON_EXISTENT_ERROR")
    assert error is None


def test_error_response_config_reset():
    # Test that adding custom errors doesn't affect the original ERROR_MESSAGES
    original_val_error = ERROR_MESSAGES["VAL_ERROR"]
    ErrorResponseConfig.add_custom_error("VAL_ERROR", "Custom validation error")
    
    # Verify the custom error was added
    error = ErrorResponseConfig.get_error("VAL_ERROR")
    assert error is not None
    assert error.message == "Custom validation error"

    # Reset the error to its original value
    ErrorResponseConfig.add_custom_error("VAL_ERROR", original_val_error)
    error = ErrorResponseConfig.get_error("VAL_ERROR")
    assert error is not None
    assert error.message == original_val_error 