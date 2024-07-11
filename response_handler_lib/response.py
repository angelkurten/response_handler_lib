import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Generic, TypeVar

from response_handler_lib.errors import ErrorResponse, ErrorResponseConfig

T = TypeVar('T')


@dataclass
class Response(Generic[T]):
    errors: Optional[List[ErrorResponse]] = None
    data: Optional[T] = None

    def add_error(self, error_code: str):
        """Add an error to the response."""
        error = ErrorResponseConfig.get_error(error_code)
        if not error:
            raise ValueError(f"Error code '{error_code}' not defined.")
        if self.errors is None:
            self.errors = []
        self.errors.append(error)

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

    def to_json(self) -> str:
        """Convert the response to JSON format."""
        return json.dumps(asdict(self), default=str)