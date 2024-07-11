import pytest

from response_handler.response import Response, ResponseError, Error


def test_is_successful_true():
    """
    Test is_successful property when success is True
    """
    response = Response(success=True)
    assert response.is_successful is True


def test_is_successful_false():
    """
    Test is_successful property when success is False
    """
    response = Response(success=False)
    assert response.is_successful is False


def test_is_successful_not_set():
    """
    Test is_successful property when success is not set
    """
    response = Response()
    with pytest.raises(ResponseError):
        assert response.is_successful


def test_has_errors_true():
    """
    Test has_errors property when there are errors
    """
    error = Error(code=404, message="Not Found")
    response = Response(errors=[error])
    assert response.has_errors is True


def test_has_errors_false():
    """
    Test has_errors property when there are no errors
    """
    response = Response()
    assert response.has_errors is False


def test_error_messages():
    """
    Test error_messages property when there are errors
    """
    error1 = Error(code=404, message="Not Found")
    error2 = Error(code=500, message="Internal Server Error")
    response = Response(errors=[error1, error2])
    assert response.error_messages == ["Not Found", "Internal Server Error"]


def test_error_messages_no_errors():
    """
    Test error_messages property when there are no errors
    """
    response = Response()
    assert response.error_messages == []


def test_error_codes():
    """
    Test error_codes property when there are errors
    """
    error1 = Error(code=404, message="Not Found")
    error2 = Error(code=500, message="Internal Server Error")
    response = Response(errors=[error1, error2])
    assert response.error_codes == [404, 500]


def test_error_codes_no_errors():
    """
    Test error_codes property when there are no errors
    """
    response = Response()
    assert response.error_codes == []


def test_add_error():
    """
    Test add_error method
    """
    response = Response()
    response.add_error(code=404, message="Not Found")
    assert response.error_codes == [404]
    assert response.error_messages == ["Not Found"]
    assert response.has_errors is True
    assert response.errors == [Error(code=404, message="Not Found")]


def test_add_multiple_errors():
    """
    Test add_error method with multiple errors
    """
    response = Response()
    response.add_error(code=404, message="Not Found")
    response.add_error(code=500, message="Internal Server Error")
    assert response.error_codes == [404, 500]
    assert response.error_messages == ["Not Found", "Internal Server Error"]
    assert response.has_errors is True
    assert response.errors == [Error(code=404, message="Not Found"), Error(code=500, message="Internal Server Error")]


def test_add_error_to_exists_errors():
    """
    Test add_error method when errors already exist
    """
    error1 = Error(code=404, message="Not Found")
    response = Response(errors=[error1])
    response.add_error(code=500, message="Internal Server Error")
    assert response.error_codes == [404, 500]
    assert response.error_messages == ["Not Found", "Internal Server Error"]
    assert response.has_errors is True
    assert response.errors == [Error(code=404, message="Not Found"), Error(code=500, message="Internal Server Error")]


def test_change_success():
    """
    Test changing success value
    """
    response = Response(success=True)
    assert response.is_successful is True
    response.success = False
    assert response.is_successful is False
    response.success = True
    assert response.is_successful is True
