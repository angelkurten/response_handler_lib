import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Generic, TypeVar, Dict, Any
import json
import inspect

from response_handler_lib.config import Config
from response_handler_lib.errors import ErrorResponse, ErrorResponseConfig

T = TypeVar('T')


@dataclass
class Response(Generic[T]):
    errors: Optional[List[ErrorResponse]] = None
    data: Optional[T] = None
    context: Optional[Dict[str, Any]] = None

    def add_error(self, error_code: str):
        """Add an error to the response."""
        error = ErrorResponseConfig.get_error(error_code)
        if not error:
            raise ValueError(f"Error code '{error_code}' not defined.")

        frame = inspect.currentframe().f_back
        filename = os.path.basename(frame.f_globals["__file__"])
        line_number = frame.f_lineno
        class_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else None
        method_name = frame.f_code.co_name

        location = f"{filename}, {class_name}.{method_name}, line {line_number}" \
            if class_name \
            else \
            f"{filename}, {method_name}, line {line_number}"

        error_instance = ErrorResponse(code=error.code, message=error.message, where=location)

        if self.errors is None:
            self.errors = []
        self.errors.append(error_instance)

        if Config.ENABLE_LOGS:
            Config.LOGGER.error(
                f"Error added:\n"
                f"  Code: {error_instance.code}\n"
                f"  Message: {error_instance.message}\n"
                f"  Location: {error_instance.where}\n"
                f"  Context: {self.context if self.context else 'None'}"
            )

    @property
    def has_errors(self) -> bool:
        """Check if the response has errors."""
        return bool(self.errors)

    @property
    def error_messages(self) -> List[str]:
        """Get a list of error messages."""
        return [err.message for err in self.errors] if self.has_errors else []

    @property
    def error_types(self) -> List[str]:
        """Get a list of error types."""
        return [err.code for err in self.errors] if self.has_errors else []

    def add_context(self, key: str, value: Any):
        """Add context information to the response."""
        if self.context is None:
            self.context = {}
        self.context[key] = value

    def to_json(self, include_where: bool = False) -> str:
        """Convert the response to JSON format."""
        response_dict = asdict(self)
        response_dict['errors'] = response_dict['errors'] if self.errors is not None else []
        if not Config.ENABLE_CONTEXT_IN_JSON:
            response_dict.pop('context', None)

        if not include_where and not Config.ENABLE_WHERE_IN_JSON:
            for error in response_dict['errors']:
                error.pop('where', None)

        return json.dumps(response_dict, default=str)
