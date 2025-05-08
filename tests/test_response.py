import pytest
import json
from pydantic import ValidationError

from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.errors import ErrorResponseConfig
from response_handler_lib.response import Response
from response_handler_lib.config import Config, enable_context_in_json, enable_where_in_json
from response_handler_lib.errors import ErrorResponse
from response_handler_lib.either import Either, ErrorItem, Success, Failure

# Add test error code
ErrorResponseConfig.add_custom_error("TEST_ERROR", "Test error message")


def test_response_default_values():
    response = Response()
    assert response.data is None
    assert response.errors == []
    assert response.context == {}
    assert response.status_code == 200


def test_response_with_data():
    data = {"key": "value"}
    response = Response(data=data)
    assert response.data == data
    assert response.errors == []
    assert response.status_code == 200


def test_response_from_either_success():
    either = Success("test data")
    response = Response.from_either(either)
    assert response.data == "test data"
    assert response.errors == []
    assert response.status_code == 200


def test_response_from_either_failure():
    error = ErrorItem.create("TEST_ERROR", "Test error message")
    either = Failure([error])
    response = Response.from_either(either)
    assert response.data is None
    assert len(response.errors) == 1
    assert response.errors[0].code == "TEST_ERROR"
    assert response.status_code == 400


def test_response_from_either_failure_with_context():
    error = ErrorItem.create("TEST_ERROR", "Test error message", context={"key": "value"})
    either = Failure([error])
    response = Response.from_either(either)
    assert response.context == {"key": "value"}


def test_response_to_dict_success():
    data = {"key": "value"}
    response = Response(data=data)
    result = response.to_dict()
    assert result["data"] == data
    assert result["status_code"] == 200
    assert "errors" in result
    assert result["errors"] == []


def test_response_to_dict_error():
    error = ErrorItem.create("TEST_ERROR", "Test error message")
    response = Response(errors=[error])
    result = response.to_dict()
    assert result["data"] is None
    assert result["status_code"] == 400
    assert "errors" in result
    assert len(result["errors"]) == 1
    assert result["errors"][0]["code"] == "TEST_ERROR"


def test_response_to_json():
    Config.ENABLE_CONTEXT_IN_JSON = True
    data = {"key": "value"}
    response = Response(data=data)
    json_str = response.to_json()
    assert isinstance(json_str, str)
    assert json_str == '{"data":{"key":"value"},"errors":[],"context":{},"status_code":200}'
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_response_status_code_validation_error():
    error = ErrorItem.create("VAL_ERROR", "Validation error")
    response = Response(errors=[error])
    assert response.status_code == 400


def test_response_status_code_authentication_error():
    error = ErrorItem.create("AUTH_ERROR", "Authentication error")
    response = Response(errors=[error])
    assert response.status_code == 401


def test_response_status_code_forbidden_error():
    error = ErrorItem.create("FORB_ERROR", "Forbidden error")
    response = Response(errors=[error])
    assert response.status_code == 403


def test_response_status_code_not_found_error():
    error = ErrorItem.create("NOT_ERROR", "Not found error")
    response = Response(errors=[error])
    assert response.status_code == 404


def test_response_status_code_timeout_error():
    error = ErrorItem.create("TIM_ERROR", "Timeout error")
    response = Response(errors=[error])
    assert response.status_code == 408


def test_response_status_code_internal_error():
    error = ErrorItem.create("INT_ERROR", "Internal error")
    response = Response(errors=[error])
    assert response.status_code == 500


def test_response_status_code_custom_error():
    error = ErrorItem.create("CUSTOM_ERROR", "Custom error")
    response = Response(errors=[error])
    assert response.status_code == 400  # Default for unknown error types


def test_response_status_code_multiple_errors():
    errors = [
        ErrorItem.create("VAL_ERROR", "Validation error"),
        ErrorItem.create("AUTH_ERROR", "Authentication error")
    ]
    response = Response(errors=errors)
    # Should keep the first error's status code
    assert response.status_code == 400


def test_response_with_none_errors():
    response = Response(data={"key": "value"})
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_context():
    response = Response(data={"key": "value"})
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_context():
    response = Response(data={"key": "value"}, context={})
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_errors():
    response = Response(data={"key": "value"}, errors=[])
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data():
    response = Response(data={})
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_errors():
    response = Response()
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_context():
    response = Response()
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_errors_and_context():
    response = Response(data={"key": "value"})
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_all_none():
    response = Response()
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data_and_errors():
    response = Response(data={}, errors=[])
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data_and_context():
    response = Response(data={}, context={})
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_errors_and_context():
    response = Response(data={"key": "value"}, errors=[], context={})
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_all_empty():
    response = Response(data={}, errors=[], context={})
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_empty_errors():
    response = Response(data=None, errors=[])
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_empty_context():
    response = Response(data=None, context={})
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_errors_and_none_context():
    response = Response(data={"key": "value"}, errors=[])
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_empty_errors_and_context():
    response = Response(data=None, errors=[], context={})
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data_and_none_errors_and_context():
    response = Response(data={})
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_errors_and_empty_context():
    response = Response(data=None)
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data_and_errors_and_none_context():
    response = Response(data={}, errors=[])
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_empty_errors_and_none_context():
    response = Response(data=None, errors=[])
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_empty_data_and_none_errors_and_empty_context():
    response = Response(data={})
    assert response.data == {}
    assert response.errors == []
    assert response.context == {}


def test_response_with_none_data_and_none_errors_and_none_context():
    response = Response()
    assert response.data is None
    assert response.errors == []
    assert response.context == {}


def test_response_with_enabled_context_in_json():
    Config.ENABLE_CONTEXT_IN_JSON = True
    response = Response(data={"key": "value"}, context={"context_key": "context_value"})
    json_str = response.to_json()
    assert "context" in json.loads(json_str)
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_response_with_enabled_where_in_json_and_no_errors():
    Config.ENABLE_WHERE_IN_JSON = True
    response = Response(data={"key": "value"})
    json_str = response.to_json()
    assert "errors" in json.loads(json_str)
    assert json.loads(json_str)["errors"] == []
    Config.ENABLE_WHERE_IN_JSON = False


def test_response_with_enabled_where_in_dict_and_no_errors():
    Config.ENABLE_WHERE_IN_JSON = True
    response = Response(data={"key": "value"})
    dict_data = response.to_dict()
    assert "errors" in dict_data
    assert dict_data["errors"] == []
    Config.ENABLE_WHERE_IN_JSON = False


def test_response_with_enabled_where_in_json_and_none_errors_and_context_and_where():
    Config.ENABLE_WHERE_IN_JSON = True
    response = Response(data={"key": "value"})
    error = ErrorItem.create("TEST", "Test")
    response.errors = [error]
    json_str = response.to_json()
    assert isinstance(json_str, str)
    assert '"code":"TEST"' in json_str
    assert '"message":"Test"' in json_str
    assert '"where":' in json_str
    Config.ENABLE_WHERE_IN_JSON = False


def test_response_with_enabled_where_in_dict_and_none_errors_and_context_and_where():
    Config.ENABLE_WHERE_IN_JSON = True
    response = Response(data={"key": "value"})
    error = ErrorItem.create("TEST", "Test")
    response.errors = [error]
    dict_data = response.to_dict()
    assert isinstance(dict_data, dict)
    assert dict_data["errors"][0]["code"] == "TEST"
    assert dict_data["errors"][0]["message"] == "Test"
    assert "where" in dict_data["errors"][0]
    Config.ENABLE_WHERE_IN_JSON = False


def test_response_invalid_status_code():
    with pytest.raises(ValidationError):
        Response(status_code=999)  # Invalid status code


def test_response_negative_status_code():
    with pytest.raises(ValidationError):
        Response(status_code=-1)  # Invalid status code


def test_response_model_dump():
    response = Response(data={"key": "value"})
    model_dict = response.model_dump()
    assert model_dict["data"] == {"key": "value"}
    assert model_dict["status_code"] == 200
    assert model_dict["errors"] == []
    assert model_dict["context"] == {}


def test_response_model_dump_json():
    response = Response(data={"key": "value"})
    json_str = response.model_dump_json()
    assert isinstance(json_str, str)
    assert json_str == '{"data":{"key":"value"},"errors":[],"context":{},"status_code":200}'


def test_response_to_json_with_context_disabled():
    Config.ENABLE_CONTEXT_IN_JSON = False
    response = Response(
        data={"key": "value"},
        context={"context_key": "context_value"}
    )
    json_str = response.to_json()
    assert "context" not in json_str
    assert "data" in json_str
    assert "errors" in json_str
    assert "status_code" in json_str


def test_response_to_json_with_where_disabled():
    Config.ENABLE_WHERE_IN_JSON = False
    error = ErrorItem.create("TEST_ERROR", "Test error message")
    response = Response(errors=[error])
    json_str = response.to_json()
    assert "where" not in json_str
    assert "errors" in json_str
    assert "code" in json_str
    assert "message" in json_str


def test_response_to_json_with_both_disabled():
    Config.ENABLE_CONTEXT_IN_JSON = False
    Config.ENABLE_WHERE_IN_JSON = False
    error = ErrorItem.create(
        "TEST_ERROR",
        "Test error message",
        context={"error_context": "value"}
    )
    response = Response(
        errors=[error],
        context={"response_context": "value"}
    )
    json_str = response.to_json()
    assert "context" not in json_str
    assert "where" not in json_str
    assert "errors" in json_str
    assert "code" in json_str
    assert "message" in json_str


def test_response_to_dict_with_context_disabled():
    Config.ENABLE_CONTEXT_IN_JSON = False
    response = Response(
        data={"key": "value"},
        context={"context_key": "context_value"}
    )
    result = response.to_dict()
    assert "context" not in result
    assert result["data"] == {"key": "value"}
    assert result["errors"] == []
    assert result["status_code"] == 200


def test_response_to_dict_with_where_disabled():
    Config.ENABLE_WHERE_IN_JSON = False
    error = ErrorItem.create("TEST_ERROR", "Test error message")
    response = Response(errors=[error])
    result = response.to_dict()
    assert "where" not in result["errors"][0]
    assert result["errors"][0]["code"] == "TEST_ERROR"
    assert result["errors"][0]["message"] == "Test error message"


def test_response_to_dict_with_both_disabled():
    Config.ENABLE_CONTEXT_IN_JSON = False
    Config.ENABLE_WHERE_IN_JSON = False
    error = ErrorItem.create(
        "TEST_ERROR",
        "Test error message",
        context={"error_context": "value"}
    )
    response = Response(
        errors=[error],
        context={"response_context": "value"}
    )
    result = response.to_dict()
    assert "context" not in result
    assert "where" not in result["errors"][0]
    assert result["errors"][0]["code"] == "TEST_ERROR"
    assert result["errors"][0]["message"] == "Test error message"


def test_response_from_either_invalid_type():
    with pytest.raises(ValueError, match="Invalid Either type"):
        Response.from_either("invalid_either")


def test_response_status_code_validation():
    with pytest.raises(ValidationError):
        Response(status_code=99)  # Too low

    with pytest.raises(ValidationError):
        Response(status_code=600)  # Too high

    # Valid status codes should work
    response = Response(status_code=200)
    assert response.status_code == 200

    response = Response(status_code=404)
    assert response.status_code == 404

    response = Response(status_code=500)
    assert response.status_code == 500


def test_response_with_complex_data():
    complex_data = {
        "nested": {
            "array": [1, 2, 3],
            "object": {
                "key": "value",
                "number": 42
            }
        },
        "boolean": True,
        "null": None
    }
    response = Response(data=complex_data)
    result = response.to_dict()
    assert result["data"] == complex_data
    assert result["status_code"] == 200
    assert result["errors"] == []


def test_response_with_multiple_errors_and_context():
    Config.ENABLE_CONTEXT_IN_JSON = True
    errors = [
        ErrorItem.create("TEST_ERROR", "First error", context={"error1": "context1"}),
        ErrorItem.create("TEST_ERROR", "Second error", context={"error2": "context2"})
    ]
    response = Response(
        errors=errors,
        context={"response_context": "value"}
    )
    result = response.to_dict()
    assert len(result["errors"]) == 2
    assert result["errors"][0]["code"] == "TEST_ERROR"
    assert result["errors"][1]["code"] == "TEST_ERROR"
    assert result["context"] == {"response_context": "value"}
    Config.ENABLE_CONTEXT_IN_JSON = False


def test_response_to_json_with_where_disabled_only():
    # Test to_json with only where disabled (context enabled)
    Config.ENABLE_CONTEXT_IN_JSON = True
    Config.ENABLE_WHERE_IN_JSON = False
    
    error = ErrorItem.create(
        "TEST_ERROR",
        "Test error message",
        context={"error_context": "value"}
    )
    response = Response(
        errors=[error],
        context={"response_context": "value"}
    )
    
    json_str = response.to_json()
    data = json.loads(json_str)
    
    # Context should be present (enabled)
    assert "context" in data
    assert data["context"] == {"response_context": "value"}
    assert "context" in data["errors"][0]
    assert data["errors"][0]["context"] == {"error_context": "value"}
    
    # Where should not be present (disabled)
    assert "where" not in data["errors"][0]
    
    # Reset config
    Config.ENABLE_CONTEXT_IN_JSON = False
    Config.ENABLE_WHERE_IN_JSON = True
