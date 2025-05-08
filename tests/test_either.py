import pytest
from response_handler_lib.either import Either, ErrorItem, Success, Failure
from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.config import Config


def test_either_success():
    either = Success("test")
    assert either.is_right
    assert not either.is_left
    assert either.get_right() == "test"
    assert either.get_left() is None


def test_either_failure():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    assert not either.is_right
    assert either.is_left
    assert either.get_right() is None
    assert len(either.get_left()) == 1
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[0].message == "Test error"


def test_either_failure_with_list():
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Error 1"),
        ErrorItem.create(PredefinedErrorCodes.AUTHENTICATION_ERROR, "Error 2")
    ]
    either = Failure(errors)
    assert not either.is_right
    assert either.is_left
    assert either.get_right() is None
    assert len(either.get_left()) == 2
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[1].code == PredefinedErrorCodes.AUTHENTICATION_ERROR.value


def test_either_map():
    either = Success(5)
    result = either.map(lambda x: x * 2)
    assert result.is_right
    assert result.get_right() == 10


def test_either_map_on_failure():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    result = either.map(lambda x: x * 2)
    assert not result.is_right
    assert result.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value


def test_either_flat_map():
    either = Success(5)
    result = either.flat_map(lambda x: Success(x * 2))
    assert result.is_right
    assert result.get_right() == 10


def test_either_flat_map_on_failure():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    result = either.flat_map(lambda x: Success(x * 2))
    assert not result.is_right
    assert result.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value


def test_either_to_json_success():
    either = Success({"key": "value"})
    json_str = either.to_json()
    assert json_str == '{"data": {"key": "value"}}'


def test_either_to_json_failure():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    json_str = either.to_json()
    assert json_str == '{"errors": [{"code": "VAL_001", "message": "Test error"}]}'


def test_either_to_json_failure_with_where():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    json_str = either.to_json(include_where=True)
    assert "where" in json_str
    assert "Test error" in json_str


def test_either_to_dict_success():
    either = Success({"key": "value"})
    result = either.to_dict()
    assert result == {"data": {"key": "value"}}


def test_either_to_dict_failure():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    result = either.to_dict()
    assert result == {"errors": [{"code": "VAL_001", "message": "Test error"}]}


def test_either_to_dict_failure_with_where():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Test error"))
    result = either.to_dict(include_where=True)
    assert "where" in result["errors"][0]
    assert result["errors"][0]["message"] == "Test error"


def test_either_failure_with_predefined_code():
    either = Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR))
    assert not either.is_right
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[0].message == "Validation Error"


def test_either_failure_with_custom_code():
    either = Failure(ErrorItem.create("CUSTOM_ERROR", "Custom error message"))
    assert not either.is_right
    assert either.get_left()[0].code == "CUSTOM_ERROR"
    assert either.get_left()[0].message == "Custom error message"


def test_either_failure_with_list_of_errors():
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Error 1"),
        ErrorItem.create(PredefinedErrorCodes.AUTHENTICATION_ERROR, "Error 2")
    ]
    either = Failure(errors)
    assert not either.is_right
    assert len(either.get_left()) == 2
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[1].code == PredefinedErrorCodes.AUTHENTICATION_ERROR.value


def test_either_failure_with_predefined_codes():
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR),
        ErrorItem.create(PredefinedErrorCodes.AUTHENTICATION_ERROR)
    ]
    either = Failure(errors)
    assert not either.is_right
    assert len(either.get_left()) == 2
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[1].code == PredefinedErrorCodes.AUTHENTICATION_ERROR.value


def test_either_failure_with_mixed_codes():
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR),
        ErrorItem.create("CUSTOM_ERROR", "Custom error")
    ]
    either = Failure(errors)
    assert not either.is_right
    assert len(either.get_left()) == 2
    assert either.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert either.get_left()[1].code == "CUSTOM_ERROR"


def test_either_success_creation():
    # Test direct Success creation
    success = Success("test")
    assert success.get_right() == "test"
    assert success.get_left() is None
    assert success.is_right is True
    assert success.is_left is False


def test_either_failure_creation():
    # Test direct Failure creation
    error = ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR)
    failure = Failure(error)
    assert failure.get_right() is None
    assert failure.get_left() == [error]
    assert failure.is_right is False
    assert failure.is_left is True


def test_either_failure_with_invalid_error():
    # Test Failure creation with invalid error type
    with pytest.raises(ValueError, match="Error must be an ErrorItem or list of ErrorItem"):
        Failure("invalid_error")


def test_either_map_with_complex_types():
    # Test map with complex data types
    success = Success({"key": "value"})
    mapped = success.map(lambda x: {**x, "new_key": "new_value"})
    assert mapped.get_right() == {"key": "value", "new_key": "new_value"}


def test_either_flat_map_with_complex_types():
    # Test flat_map with complex data types
    success = Success({"key": "value"})
    mapped = success.flat_map(lambda x: Success({**x, "new_key": "new_value"}))
    assert mapped.get_right() == {"key": "value", "new_key": "new_value"}


def test_either_to_json_with_complex_data():
    # Test to_json with complex data types
    success = Success({"nested": {"key": "value"}})
    json_str = success.to_json()
    assert '"data": {"nested": {"key": "value"}}' in json_str


def test_either_to_dict_with_complex_data():
    # Test to_dict with complex data types
    success = Success({"nested": {"key": "value"}})
    dict_data = success.to_dict()
    assert dict_data == {"data": {"nested": {"key": "value"}}}


def test_either_failure_with_multiple_errors():
    # Test Failure with multiple errors
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR),
        ErrorItem.create(PredefinedErrorCodes.NOT_FOUND)
    ]
    failure = Failure(errors)
    assert len(failure.get_left()) == 2
    assert failure.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert failure.get_left()[1].code == PredefinedErrorCodes.NOT_FOUND.value


def test_either_failure_to_json_with_multiple_errors():
    # Test to_json with multiple errors
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR),
        ErrorItem.create(PredefinedErrorCodes.NOT_FOUND)
    ]
    failure = Failure(errors)
    json_str = failure.to_json()
    assert '"errors": [' in json_str
    assert PredefinedErrorCodes.VALIDATION_ERROR.value in json_str
    assert PredefinedErrorCodes.NOT_FOUND.value in json_str


def test_either_failure_to_dict_with_multiple_errors():
    # Test to_dict with multiple errors
    errors = [
        ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR),
        ErrorItem.create(PredefinedErrorCodes.NOT_FOUND)
    ]
    failure = Failure(errors)
    dict_data = failure.to_dict()
    assert len(dict_data["errors"]) == 2
    assert dict_data["errors"][0]["code"] == PredefinedErrorCodes.VALIDATION_ERROR.value
    assert dict_data["errors"][1]["code"] == PredefinedErrorCodes.NOT_FOUND.value


def test_either_failure_map_chain():
    # Test chaining map operations on Failure
    error = ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR)
    failure = Failure(error)
    mapped = failure.map(lambda x: x + 1).map(lambda x: x * 2)
    assert mapped.get_left() == [error]


def test_either_failure_flat_map_chain():
    # Test chaining flat_map operations on Failure
    error = ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR)
    failure = Failure(error)
    mapped = failure.flat_map(lambda x: Success(x + 1)).flat_map(lambda x: Success(x * 2))
    assert mapped.get_left() == [error]


def test_either_success_map_chain():
    # Test chaining map operations on Success
    success = Success(5)
    mapped = success.map(lambda x: x + 1).map(lambda x: x * 2)
    assert mapped.get_right() == 12


def test_either_success_flat_map_chain():
    # Test chaining flat_map operations on Success
    success = Success(5)
    mapped = success.flat_map(lambda x: Success(x + 1)).flat_map(lambda x: Success(x * 2))
    assert mapped.get_right() == 12


def test_failure_with_invalid_error_type():
    with pytest.raises(ValueError, match="Error must be an ErrorItem or list of ErrorItem"):
        Failure(error="invalid error")


def test_error_item_create_with_string_code():
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message")
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "Custom error message"
    assert error.where is not None


def test_error_item_create_with_predefined_code_no_message():
    error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST)
    assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
    assert error.message == "Bad Request"
    assert error.where is not None


def test_error_item_create_with_string_code_no_message():
    error = ErrorItem.create("CUSTOM_ERROR")
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "An error occurred"
    assert error.where is not None


def test_error_item_create_with_predefined_code_and_no_message():
    error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST)
    assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
    assert error.message == "Bad Request"
    assert error.where is not None


def test_error_item_create_with_string_code_and_no_message():
    error = ErrorItem.create("CUSTOM_ERROR")
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "An error occurred"
    assert error.where is not None


class TestClass:
    def test_error_item_create_with_class_name(self):
        error = ErrorItem.create("CUSTOM_ERROR")
        assert "TestClass.test_error_item_create_with_class_name" in error.where


def test_error_item_create_with_predefined_code_and_message():
    error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, "Custom message")
    assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
    assert error.message == "Custom message"
    assert error.where is not None


def test_error_item_create_with_predefined_code_and_no_message_in_class():
    class TestClass:
        def test_method(self):
            error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST)
            assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
            assert error.message == "Bad Request"
            assert error.where is not None
            assert "TestClass.test_method" in error.where
    
    test_instance = TestClass()
    test_instance.test_method()


def test_error_item_create_with_string_code_and_no_message_in_class():
    class TestClass:
        def test_method(self):
            error = ErrorItem.create("CUSTOM_ERROR")
            assert error.code == "CUSTOM_ERROR"
            assert error.message == "An error occurred"
            assert error.where is not None
            assert "TestClass.test_method" in error.where
    
    test_instance = TestClass()
    test_instance.test_method()


def test_error_item_create_with_predefined_code_and_no_message_in_function():
    def test_function():
        error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST)
        assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
        assert error.message == "Bad Request"
        assert error.where is not None
        assert "test_function" in error.where
    
    test_function()


def test_error_item_create_with_string_code_and_no_message_in_function():
    def test_function():
        error = ErrorItem.create("CUSTOM_ERROR")
        assert error.code == "CUSTOM_ERROR"
        assert error.message == "An error occurred"
        assert error.where is not None
        assert "test_function" in error.where
    
    test_function()


def test_error_item_create_with_context():
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=context)
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "Custom error message"
    assert error.where is not None
    assert error.context == context


def test_error_item_create_with_predefined_code_and_context():
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, context=context)
    assert error.code == PredefinedErrorCodes.BAD_REQUEST.value
    assert error.message == "Bad Request"
    assert error.where is not None
    assert error.context == context


def test_error_item_create_with_string_code_and_context():
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create("CUSTOM_ERROR", context=context)
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "An error occurred"
    assert error.where is not None
    assert error.context == context


def test_error_item_create_with_none_context():
    error = ErrorItem.create("CUSTOM_ERROR", context=None)
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "An error occurred"
    assert error.where is not None
    assert error.context is None


def test_error_item_create_with_empty_context():
    error = ErrorItem.create("CUSTOM_ERROR", context={})
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "An error occurred"
    assert error.where is not None
    assert error.context == {}


def test_error_item_create_with_complex_context():
    context = {
        "user": {
            "id": "123",
            "name": "Test User"
        },
        "action": "test",
        "metadata": {
            "timestamp": "2024-01-01",
            "version": "1.0"
        }
    }
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=context)
    assert error.code == "CUSTOM_ERROR"
    assert error.message == "Custom error message"
    assert error.where is not None
    assert error.context == context


def test_error_item_create_with_context_logging(caplog):
    Config.ENABLE_LOGS = True
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=context)
    
    assert any("Error created" in record.message for record in caplog.records)
    assert any("Code: CUSTOM_ERROR" in record.message for record in caplog.records)
    assert any("Context: {'user_id': '123', 'action': 'test'}" in record.message for record in caplog.records)
    
    Config.ENABLE_LOGS = False


def test_error_item_to_dict_with_context():
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=context)
    
    # Test without context enabled
    Config.ENABLE_CONTEXT_IN_JSON = False
    result = error.to_dict()
    assert "context" not in result
    
    # Test with context enabled
    Config.ENABLE_CONTEXT_IN_JSON = True
    result = error.to_dict()
    assert "context" in result
    assert result["context"] == context
    
    # Reset config
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_error_item_to_dict_with_context_and_where():
    context = {"user_id": "123", "action": "test"}
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=context)
    
    # Test with both context and where enabled
    Config.ENABLE_CONTEXT_IN_JSON = True
    result = error.to_dict(include_where=True)
    assert "context" in result
    assert "where" in result
    assert result["context"] == context
    assert result["where"] == error.where
    
    # Reset config
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_error_item_to_dict_with_none_context():
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context=None)
    
    # Test with context enabled but no context
    Config.ENABLE_CONTEXT_IN_JSON = True
    result = error.to_dict()
    assert "context" not in result
    
    # Reset config
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_error_item_to_dict_with_empty_context():
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error message", context={})
    
    # Test with context enabled but empty context
    Config.ENABLE_CONTEXT_IN_JSON = True
    result = error.to_dict()
    assert "context" not in result
    
    # Reset config
    Config.ENABLE_CONTEXT_IN_JSON = False 