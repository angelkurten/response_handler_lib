import pytest
import requests
import requests_mock
from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.either import Either, ErrorItem
from response_handler_lib.http_interceptor import HTTPInterceptor
from response_handler_lib.either import Success, Failure
from requests.exceptions import JSONDecodeError
from response_handler_lib.config import Config


@pytest.fixture
def interceptor():
    return HTTPInterceptor()


def test_successful_request(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', json={"id": 1, "title": "test"})
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Success)
        assert response.get_right() == {"id": 1, "title": "test"}


def test_404_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/999', status_code=404)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/999')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.NOT_FOUND.value


def test_401_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=401)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.AUTHENTICATION_ERROR.value


def test_403_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=403)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.FORBIDDEN.value


def test_422_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=422)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value


def test_500_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=500)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.INTERNAL_ERROR.value


def test_connection_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', exc=requests.exceptions.ConnectionError)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_timeout_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', exc=requests.exceptions.Timeout)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_generic_exception(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', exc=requests.exceptions.ConnectTimeout)
        response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Failure)
        assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_post_request(interceptor):
    with requests_mock.Mocker() as m:
        m.post('https://jsonplaceholder.typicode.com/posts', json={"id": 1})
        response = interceptor.request('POST', 'https://jsonplaceholder.typicode.com/posts', data={"title": "test"})
        assert isinstance(response, Success)
        assert response.get_right() == {"id": 1}


def test_put_request(interceptor):
    with requests_mock.Mocker() as m:
        m.put('https://jsonplaceholder.typicode.com/posts/1', json={"id": 1})
        response = interceptor.request('PUT', 'https://jsonplaceholder.typicode.com/posts/1', data={"title": "test"})
        assert isinstance(response, Success)
        assert response.get_right() == {"id": 1}


def test_delete_request(interceptor):
    with requests_mock.Mocker() as m:
        m.delete('https://jsonplaceholder.typicode.com/posts/1', json={})
        response = interceptor.request('DELETE', 'https://jsonplaceholder.typicode.com/posts/1')
        assert isinstance(response, Success)
        assert response.get_right() == {}


def test_request_with_empty_response(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/empty"
    requests_mock.get(url, text="")
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Success)
    assert response.get_right() == {}


def test_request_with_connection_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/connection-error"
    requests_mock.get(url, exc=requests.exceptions.ConnectionError("Connection error"))
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_request_with_timeout_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/timeout-error"
    requests_mock.get(url, exc=requests.exceptions.Timeout("Timeout error"))
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_request_with_generic_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/generic-error"
    requests_mock.get(url, exc=Exception("Generic error"))
    
    Config.ENABLE_LOGS = True
    response = interceptor.request("GET", url)
    Config.ENABLE_LOGS = False
    
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.INTERNAL_ERROR.value


def test_request_with_non_json_response(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/text"
    plain_text = "Hello, World!"
    requests_mock.get(url, text=plain_text)
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Success)
    assert response.get_right() == {"text": plain_text}


def test_request_with_params(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/params"
    requests_mock.get(url, json={"args": {"key": "value"}})
    
    response = interceptor.request(
        "GET",
        url,
        params={"key": "value"},
        timeout=5
    )
    assert isinstance(response, Success)
    assert response.get_right()["args"]["key"] == "value"


def test_request_with_headers(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/headers"
    headers = {"Custom-Header": "test-value"}
    requests_mock.get(url, json={"headers": headers})
    
    response = interceptor.request(
        "GET",
        url,
        headers=headers,
        timeout=5
    )
    assert isinstance(response, Success)
    assert response.get_right()["headers"]["Custom-Header"] == "test-value"


def test_request_with_json_data(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/json"
    data = {"test": "data"}
    requests_mock.post(url, json={"json": data})
    
    response = interceptor.request(
        "POST",
        url,
        json=data,
        timeout=5
    )
    assert isinstance(response, Success)
    assert response.get_right()["json"] == data


def test_request_with_form_data(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/form"
    data = {"test": "data"}
    requests_mock.post(url, json={"form": data})
    
    response = interceptor.request(
        "POST",
        url,
        data=data,
        timeout=5
    )
    assert isinstance(response, Success)
    assert response.get_right()["form"] == data


def test_logging_on_generic_error(caplog):
    interceptor = HTTPInterceptor()
    response = interceptor.request("GET", None)  # This will cause an error
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_custom_session():
    interceptor = HTTPInterceptor()
    assert isinstance(interceptor.session, requests.Session)
    
    # Test session is being used
    response = interceptor.request("GET", "https://api.example.com/test")
    assert isinstance(response, Failure)  # Will fail because URL doesn't exist


def test_request_with_invalid_method():
    interceptor = HTTPInterceptor()
    response = interceptor.request("INVALID", "https://api.example.com/test")
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_request_with_invalid_url():
    interceptor = HTTPInterceptor()
    response = interceptor.request("GET", "invalid-url")
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value


def test_request_with_invalid_json(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/invalid-json"
    requests_mock.get(url, text="{invalid json")
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Success)
    assert response.get_right() == {"text": "{invalid json"}


def test_request_with_empty_json(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/empty-json"
    requests_mock.get(url, json={})
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Success)
    assert response.get_right() == {}


def test_request_with_none_data(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/none-data"
    requests_mock.post(url, json={"data": None})
    
    response = interceptor.request("POST", url, data=None)
    assert isinstance(response, Success)
    assert response.get_right() == {"data": None}


def test_request_with_none_json(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/none-json"
    requests_mock.post(url, json={"json": None})
    
    response = interceptor.request("POST", url, json=None)
    assert isinstance(response, Success)
    assert response.get_right() == {"json": None}


def test_request_with_none_headers(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/none-headers"
    requests_mock.get(url, json={"headers": None})
    
    response = interceptor.request("GET", url, headers=None)
    assert isinstance(response, Success)
    assert response.get_right() == {"headers": None}


def test_request_with_none_params(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/none-params"
    requests_mock.get(url, json={"params": None})
    
    response = interceptor.request("GET", url, params=None)
    assert isinstance(response, Success)
    assert response.get_right() == {"params": None}


def test_request_with_custom_timeout(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/timeout"
    requests_mock.get(url, json={"timeout": 10})
    
    response = interceptor.request("GET", url, timeout=10)
    assert isinstance(response, Success)
    assert response.get_right() == {"timeout": 10}


def test_request_with_include_where(requests_mock):
    interceptor = HTTPInterceptor(include_where=True)
    url = "https://api.example.com/error"
    requests_mock.get(url, status_code=404)
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert "where" in response.get_left()[0].to_dict(include_where=True)


def test_request_with_validation_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/validation-error"
    requests_mock.get(url, status_code=422)
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.VALIDATION_ERROR.value


def test_request_with_internal_server_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/internal-error"
    requests_mock.get(url, status_code=500)
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.INTERNAL_ERROR.value


def test_request_with_other_http_error(requests_mock):
    interceptor = HTTPInterceptor()
    url = "https://api.example.com/other-error"
    requests_mock.get(url, status_code=418)  # I'm a teapot
    
    response = interceptor.request("GET", url)
    assert isinstance(response, Failure)
    assert response.get_left()[0].code == PredefinedErrorCodes.BAD_REQUEST.value
