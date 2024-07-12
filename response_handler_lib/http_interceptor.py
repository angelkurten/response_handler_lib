import logging

import requests
from requests.exceptions import HTTPError

from response_handler_lib.config import Config
from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.response import Response


class HTTPInterceptor:
    def __init__(self, include_where=False):
        self.include_where = include_where
        self.response = Response()

    def request(self, method, url, **kwargs):
        resp = None
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            if resp.status_code != 204:
                self.response.data = resp.json()
        except HTTPError as http_err:
            self.handle_http_error(http_err, resp)
        except Exception as err:
            self.handle_generic_error(err)
        return self.response.to_json()

    def handle_http_error(self, http_err, resp):
        if resp.status_code == 400:
            self.response.add_error(PredefinedErrorCodes.BAD_REQUEST.value)
        elif resp.status_code == 404:
            self.response.add_error(PredefinedErrorCodes.NOT_FOUND.value)
        elif resp.status_code == 500:
            self.response.add_error(PredefinedErrorCodes.INTERNAL_ERROR.value)
        else:
            self.response.add_error(PredefinedErrorCodes.INTERNAL_ERROR.value)
        if Config.ENABLE_LOGS:
            Config.LOGGER.error(f"HTTP error occurred: {http_err}")

    def handle_generic_error(self, err):
        self.response.add_error(PredefinedErrorCodes.INTERNAL_ERROR.value)
        if Config.ENABLE_LOGS:
            Config.LOGGER.error(f"HTTP error occurred: {err}")
