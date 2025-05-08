from dataclasses import dataclass, asdict
from typing import TypeVar, Generic, Optional, List, Dict, Any, Union
import json
import os
import inspect

from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.config import Config

L = TypeVar('L')  # Tipo para el error
R = TypeVar('R')  # Tipo para el éxito


@dataclass
class ErrorItem:
    code: str
    message: str
    where: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    @classmethod
    def create(cls, code: Union[str, PredefinedErrorCodes], message: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> 'ErrorItem':
        frame = inspect.currentframe().f_back
        filename = os.path.basename(frame.f_globals["__file__"])
        line_number = frame.f_lineno
        class_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else None
        method_name = frame.f_code.co_name

        location = f"{filename}, {class_name}.{method_name}, line {line_number}" \
            if class_name \
            else \
            f"{filename}, {method_name}, line {line_number}"

        if isinstance(code, PredefinedErrorCodes):
            error_code = code.value
            error_message = message or code.name.replace('_', ' ').title()
        else:
            error_code = code
            error_message = message or "An error occurred"

        error = cls(code=error_code, message=error_message, where=location, context=context)
        
        if Config.ENABLE_LOGS:
            Config.LOGGER.error(
                f"Error created:\n"
                f"  Code: {error.code}\n"
                f"  Message: {error.message}\n"
                f"  Location: {error.where}\n"
                f"  Context: {error.context if error.context else 'None'}"
            )
            
        return error

    def to_dict(self, include_where: bool = False) -> Dict[str, Any]:
        result = {
            "code": self.code,
            "message": self.message
        }
        if include_where and self.where:
            result["where"] = self.where
        if Config.ENABLE_CONTEXT_IN_JSON and self.context:
            result["context"] = self.context
        return result


class Either(Generic[L, R]):
    @staticmethod
    def success(value: R) -> 'Success[L, R]':
        return Success(value)

    @staticmethod
    def failure(error: Union[ErrorItem, List[ErrorItem]]) -> 'Failure[L, R]':
        return Failure(error)


class Success(Either[L, R]):
    def __init__(self, value: R):
        self._value = value

    @property
    def is_right(self) -> bool:
        return True

    @property
    def is_left(self) -> bool:
        return False

    def get_right(self) -> R:
        return self._value

    def get_left(self) -> None:
        return None

    def map(self, f) -> 'Success[L, R]':
        return Success(f(self._value))

    def flat_map(self, f) -> Either[L, R]:
        return f(self._value)

    def to_json(self, include_where: bool = False) -> str:
        return json.dumps({"data": self._value})

    def to_dict(self, include_where: bool = False) -> Dict[str, Any]:
        return {"data": self._value}


class Failure(Either[L, R]):
    def __init__(self, error: Union[ErrorItem, List[ErrorItem]]):
        if isinstance(error, ErrorItem):
            self._errors = [error]
        elif isinstance(error, list):
            self._errors = error
        else:
            raise ValueError("Error must be an ErrorItem or list of ErrorItem")

    @property
    def is_right(self) -> bool:
        return False

    @property
    def is_left(self) -> bool:
        return True

    def get_right(self) -> None:
        return None

    def get_left(self) -> List[ErrorItem]:
        return self._errors

    def map(self, f) -> 'Failure[L, R]':
        return self

    def flat_map(self, f) -> 'Failure[L, R]':
        return self

    def to_json(self, include_where: bool = False) -> str:
        return json.dumps({"errors": [error.to_dict(include_where) for error in self._errors]})

    def to_dict(self, include_where: bool = False) -> Dict[str, Any]:
        return {"errors": [error.to_dict(include_where) for error in self._errors]} 