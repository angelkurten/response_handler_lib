from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict
from .either import Either, ErrorItem, Success, Failure

class Response(BaseModel):
    """
    A class representing a final response, typically used for HTTP responses.
    This class is designed to be the final output format, while Either is used
    for intermediate error handling in the business logic layers.
    """
    data: Optional[Any] = None
    errors: List[ErrorItem] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    status_code: int = Field(default=200)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "data": {"key": "value"},
                "errors": [],
                "context": {},
                "status_code": 200
            }
        }
    )

    @field_validator('status_code')
    @classmethod
    def validate_status_code(cls, v: int) -> int:
        """Validate that status code is a valid HTTP status code."""
        if not (100 <= v <= 599):
            raise ValueError('Status code must be between 100 and 599')
        return v

    def __init__(self, **data):
        super().__init__(**data)
        if self.errors:
            self._update_status_code(self.errors[0].code)

    def _update_status_code(self, error_code: str) -> None:
        """Update status code based on error type."""
        status_map = {
            'VAL_ERROR': 400,
            'AUTH_ERROR': 401,
            'FORB_ERROR': 403,
            'NOT_ERROR': 404,
            'TIM_ERROR': 408,
            'INT_ERROR': 500
        }
        self.status_code = status_map.get(error_code, 400)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary format."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert the response to JSON format."""
        return self.model_dump_json()

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
            response = cls(errors=either._errors)
            if either._errors and either._errors[0].context:
                response.context.update(either._errors[0].context)
            return response
        raise ValueError("Invalid Either type")
