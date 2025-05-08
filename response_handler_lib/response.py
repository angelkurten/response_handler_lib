import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Generic, TypeVar, Dict, Any, Union
import json

from response_handler_lib.config import Config
from response_handler_lib.either import Either, ErrorItem, Success, Failure

T = TypeVar('T')


@dataclass
class Response(Generic[T]):
    """
    A class representing a final response, typically used for HTTP responses.
    This class is designed to be the final output format, while Either is used
    for intermediate error handling in the business logic layers.
    """
    errors: Optional[List[ErrorItem]] = None
    data: Optional[T] = None
    context: Optional[Dict[str, Any]] = None
    status_code: int = 200

    def __post_init__(self):
        """Initialize default values after dataclass initialization."""
        if self.errors is None:
            self.errors = []
        if self.context is None:
            self.context = {}
        # Update status code if there are errors
        if self.errors:
            self._update_status_code(self.errors[0].code)

    def _update_status_code(self, error_code: str) -> None:
        """Update status code based on error type."""
        if error_code.startswith('VAL_'):
            self.status_code = 400  # Bad Request
        elif error_code.startswith('AUTH_'):
            self.status_code = 401  # Unauthorized
        elif error_code.startswith('FORB_'):
            self.status_code = 403  # Forbidden
        elif error_code.startswith('NOT_'):
            self.status_code = 404  # Not Found
        elif error_code.startswith('TIM_'):
            self.status_code = 408  # Request Timeout
        elif error_code.startswith('INT_'):
            self.status_code = 500  # Internal Server Error
        else:
            self.status_code = 400  # Default to Bad Request

    def to_dict(self, include_where: bool = False) -> dict:
        """Convert the response to a dictionary format."""
        result = {
            "status_code": self.status_code,
            "data": self.data,
            "errors": [
                {
                    "code": error.code,
                    "message": error.message,
                    "where": error.where if include_where or Config.ENABLE_WHERE_IN_JSON else None
                }
                for error in self.errors
            ]
        }
        if Config.ENABLE_CONTEXT_IN_JSON and self.context:
            result["context"] = self.context
        return result

    def to_json(self, include_where: bool = False) -> str:
        """Convert the response to JSON format."""
        return json.dumps(self.to_dict(include_where), default=str)

    @classmethod
    def from_either(cls, either: Either) -> 'Response':
        """
        Create a Response from an Either.
        This is useful when converting from intermediate error handling
        to a final response format.
        """
        if isinstance(either, Success):
            return cls(data=either._value)
        elif isinstance(either, Failure):
            response = cls()
            for error in either._errors:
                response.errors.append(error)
                if error.context:
                    response.context.update(error.context)
                response._update_status_code(error.code)
            return response
        else:
            raise ValueError("Invalid Either type")
