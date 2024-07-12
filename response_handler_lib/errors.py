from dataclasses import dataclass
from typing import Dict, Optional

from response_handler_lib.error_codes import ERROR_MESSAGES


@dataclass
class ErrorResponse:
    code: str
    message: str
    where: Optional[str] = None


class ErrorResponseConfig:
    _errors: Dict[str, str] = ERROR_MESSAGES

    @classmethod
    def add_custom_error(cls, code: str, message: str):
        cls._errors[code] = message

    @classmethod
    def add_custom_errors(cls, errors: Dict[str, str]):
        for code, message in errors.items():
            cls.add_custom_error(code, message)

    @classmethod
    def get_error(cls, code: str) -> Optional[ErrorResponse]:
        message = cls._errors.get(code)
        return ErrorResponse(code=code, message=message) if message else None
