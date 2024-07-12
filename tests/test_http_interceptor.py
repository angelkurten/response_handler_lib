import pytest
import requests
import requests_mock
from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.response import Response
from response_handler_lib.http_interceptor import HTTPInterceptor


@pytest.fixture
def interceptor():
    return HTTPInterceptor()


def test_successful_get_request(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', json={'title': 'foo'})

        response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response(data={'title': 'foo'})

        assert response_json == response.to_json()


def test_400_bad_request(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=400)

        response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response()
        response.add_error(PredefinedErrorCodes.BAD_REQUEST.value)

        assert response_json == response.to_json()


def test_404_not_found(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=404)

        response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response()
        response.add_error(PredefinedErrorCodes.NOT_FOUND.value)

        assert response_json == response.to_json()


def test_500_internal_error(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', status_code=500)

        response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response()
        response.add_error(PredefinedErrorCodes.INTERNAL_ERROR.value)

        assert response_json == response.to_json()


def test_generic_exception(interceptor):
    with requests_mock.Mocker() as m:
        m.get('https://jsonplaceholder.typicode.com/posts/1', exc=requests.exceptions.ConnectTimeout)

        response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response()
        response.add_error(PredefinedErrorCodes.INTERNAL_ERROR.value)

        assert response_json == response.to_json()


def test_post_request(interceptor):
    with requests_mock.Mocker() as m:
        m.post('https://jsonplaceholder.typicode.com/posts', json={'id': 1, 'title': 'foo'}, status_code=201)

        response_json = interceptor.request('POST', 'https://jsonplaceholder.typicode.com/posts', json={'title': 'foo'})
        response = Response(data={'id': 1, 'title': 'foo'})

        assert response_json == response.to_json()


def test_put_request(interceptor):
    with requests_mock.Mocker() as m:
        m.put('https://jsonplaceholder.typicode.com/posts/1', json={'id': 1, 'title': 'bar'}, status_code=200)

        response_json = interceptor.request('PUT', 'https://jsonplaceholder.typicode.com/posts/1',
                                            json={'title': 'bar'})
        response = Response(data={'id': 1, 'title': 'bar'})

        assert response_json == response.to_json()


def test_delete_request(interceptor):
    with requests_mock.Mocker() as m:
        m.delete('https://jsonplaceholder.typicode.com/posts/1', status_code=204)

        response_json = interceptor.request('DELETE', 'https://jsonplaceholder.typicode.com/posts/1')
        response = Response(data=None)

        assert response_json == response.to_json()
