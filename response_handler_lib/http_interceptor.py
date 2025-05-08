import logging
import requests
from requests.exceptions import HTTPError, JSONDecodeError
from typing import Optional, Dict, Any, Union

from response_handler_lib.config import Config
from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.either import Either, ErrorItem, Success, Failure


class HTTPInterceptor:
    def __init__(self, include_where=False):
        self.include_where = include_where
        self.session = requests.Session()

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> Either[ErrorItem, Any]:
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json or data,
                headers=headers,
                timeout=timeout
            )
            resp.raise_for_status()
            
            # Si la respuesta está vacía, devolver un diccionario vacío
            if not resp.content:
                return Success({})
                
            try:
                return Success(resp.json())
            except JSONDecodeError:
                # Si no es JSON, devolver el texto de la respuesta
                return Success({"text": resp.text})
                
        except requests.exceptions.RequestException as err:
            return self.handle_request_error(err)
        except Exception as err:
            return self.handle_generic_error(err)

    def handle_request_error(self, err: requests.exceptions.RequestException) -> Either[ErrorItem, Any]:
        if isinstance(err, requests.exceptions.ConnectionError):
            return Failure(ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, str(err)))
        elif isinstance(err, requests.exceptions.Timeout):
            return Failure(ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, str(err)))
        elif isinstance(err, requests.exceptions.HTTPError):
            if err.response.status_code == 401:
                return Failure(ErrorItem.create(PredefinedErrorCodes.AUTHENTICATION_ERROR, str(err)))
            elif err.response.status_code == 403:
                return Failure(ErrorItem.create(PredefinedErrorCodes.FORBIDDEN, str(err)))
            elif err.response.status_code == 404:
                return Failure(ErrorItem.create(PredefinedErrorCodes.NOT_FOUND, str(err)))
            elif err.response.status_code == 422:
                return Failure(ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, str(err)))
            elif err.response.status_code >= 500:
                return Failure(ErrorItem.create(PredefinedErrorCodes.INTERNAL_ERROR, str(err)))
            else:
                return Failure(ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, str(err)))
        else:
            return Failure(ErrorItem.create(PredefinedErrorCodes.BAD_REQUEST, str(err)))

    def handle_generic_error(self, err: Exception) -> Either[ErrorItem, Any]:
        if Config.ENABLE_LOGS:
            Config.LOGGER.error(f"Generic error occurred: {err}")

        return Failure(ErrorItem.create(PredefinedErrorCodes.INTERNAL_ERROR, str(err)))
