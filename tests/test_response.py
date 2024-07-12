import pytest

from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.errors import ErrorResponseConfig
from response_handler_lib.response import Response


def test_predefined_error():
    response = Response()
    response.add_error(PredefinedErrorCodes.VALIDATION_ERROR.value)

    assert response.has_errors is True
    assert response.error_messages == ["Validation failed."]
    assert response.error_types == ["VAL_001"]


def test_add_custom_error():
    ErrorResponseConfig.add_custom_error("CUS_ERR1", "Custom error message 1.")
    response = Response()
    response.add_error("CUS_ERR1")

    assert response.has_errors is True
    assert response.error_messages == ["Custom error message 1."]
    assert response.error_types == ["CUS_ERR1"]


def test_add_multiple_custom_errors():
    custom_errors = {
        "CUS_ERR2": "Custom error message 2.",
        "CUS_ERR3": "Custom error message 3."
    }
    ErrorResponseConfig.add_custom_errors(custom_errors)
    response = Response()
    response.add_error("CUS_ERR2")
    response.add_error("CUS_ERR3")

    assert response.has_errors is True
    assert response.error_messages == ["Custom error message 2.", "Custom error message 3."]
    assert response.error_types == ["CUS_ERR2", "CUS_ERR3"]


def test_error_not_defined():
    response = Response()
    with pytest.raises(ValueError, match="Error code 'NOT_DEFINED' not defined."):
        response.add_error("NOT_DEFINED")


def test_response_without_errors():
    response = Response()

    assert response.has_errors is False
    assert response.error_messages == []
    assert response.error_types == []


def test_successful_response_with_data():
    response = Response(data="Sample data")
    assert response.data == "Sample data"
    assert response.has_errors is False
    assert response.error_messages == []
    assert response.error_types == []


def test_response_with_mixed_errors_and_data():
    ErrorResponseConfig.add_custom_error("CUS_ERR4", "Custom error message 4.")
    response = Response(data="Sample data")
    response.add_error("CUS_ERR4")
    response.add_error(PredefinedErrorCodes.REQUEST_TIMEOUT.value)

    assert response.data == "Sample data"
    assert response.has_errors is True
    assert response.error_messages == ["Custom error message 4.", "Request timed out."]
    assert response.error_types == ["CUS_ERR4", "TIM_006"]


def test_to_json():
    ErrorResponseConfig.add_custom_error("CUS_ERR5", "Custom error message 5.")
    response = Response(data={"key": "value"})
    response.add_error("CUS_ERR5")

    expected_json = '{"errors": [{"code": "CUS_ERR5", "message": "Custom error message 5."}], "data": {"key": "value"}}'
    assert response.to_json() == expected_json


def test_to_json_include_where():
    ErrorResponseConfig.add_custom_error("CUS_ERR6", "Custom error message 6.")
    response = Response(data={"key": "value"})
    response.add_error("CUS_ERR6")

    json_output = response.to_json(include_where=True)
    assert '"code": "CUS_ERR6"' in json_output
    assert '"message": "Custom error message 6."' in json_output
    assert '"where":' in json_output
