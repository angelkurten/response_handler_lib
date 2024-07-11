from dataclasses import dataclass
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')


class ResponseError(Exception):
    """
    Custom exception for response errors.
    """

    def __init__(self, message: str):
        super().__init__(message)


@dataclass
class Error:
    code: int
    message: str


@dataclass
class Response(Generic[T]):
    success: Optional[bool] = None
    errors: Optional[List[Error]] = None
    data: Optional[T] = None

    @property
    def is_successful(self) -> bool:
        """
        Check if the response is successful.

        :return: True if the response is successful, False otherwise.
        :rtype: bool
        """
        if self.success is None:
            raise ResponseError(f"{self.__class__.__name__} success field is not set")

        return self.success

    def add_error(self, code: int, message: str):
        """
        Add an error to the response.

        :param code: Error code.
        :type code: int
        :param message: Error message.
        :type message: str
        """
        if self.errors is None:
            self.errors = []

        self.errors.append(Error(code=code, message=message))

    @property
    def has_errors(self) -> bool:
        """
        Check if the response has errors.

        :return: True if there are errors, False otherwise.
        :rtype: bool
        """
        return bool(self.errors)

    @property
    def error_messages(self) -> List[str]:
        """
        Get a list of error messages
        :return: List of error messages
        :rtype: List[str]
        """
        if self.has_errors:
            return [err.message for err in self.errors]
        return []

    @property
    def error_codes(self) -> List[int]:
        """
        Get a list of error codes
        :return: List of error codes
        :rtype: List[int]
        """
        if self.has_errors:
            return [err.code for err in self.errors]
        return []
