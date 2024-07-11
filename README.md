
# response_handler

A package for handling responses with potential errors and generic data.

## Features

- Custom `Response` class for handling responses with success status, errors, and data.
- Custom `Error` class for defining error codes and messages.
- Custom `ResponseError` exception for handling response-related errors.
- Utilities for adding errors, checking success status, and retrieving error messages and codes.

## Installation

You can install `response_handler` via pip:

```sh
pip install response_handler
```

## Usage

### Importing the Package

To use the `Response` class and related utilities, import them from the `response_handler` package:

```python
from response_handler import Response, Error, ResponseError
```

### Creating a Successful Response

Create a `Response` object with `success` set to `True` and provide any data:

```python
response = Response(success=True, data="Some data")
if response.is_successful:
    print("Response is successful")
    print("Data:", response.data)
```

### Creating a Failed Response

Create a `Response` object with `success` set to `False`:

```python
response = Response(success=False)
if not response.is_successful:
    print("Response failed")
```

### Adding Errors to a Response

Add errors to a response using the `add_error` method:

```python
response = Response(success=False)
response.add_error(404, "Not Found")
response.add_error(500, "Internal Server Error")

if response.has_errors:
    print("Errors:")
    for code, message in zip(response.error_codes, response.error_messages):
        print(f"Error {code}: {message}")
```

### Handling Missing Success Field

If the `success` field is not set, accessing `is_successful` raises a `ResponseError`:

```python
response = Response()

try:
    print(response.is_successful)
except ResponseError as e:
    print("Caught an error:", str(e))
```

## API Reference

### Classes

#### `Response`

A generic class for handling responses.

##### Attributes:

- `success` (`Optional[bool]`): Indicates whether the response is successful.
- `errors` (`Optional[List[Error]]`): A list of errors in the response.
- `data` (`Optional[T]`): The data in the response.

##### Methods:

- `is_successful` (`bool`): Checks if the response is successful. Raises `ResponseError` if `success` is not set.
- `add_error(code: int, message: str)`: Adds an error to the response.
- `has_errors` (`bool`): Checks if the response has errors.
- `error_messages` (`List[str]`): Retrieves a list of error messages.
- `error_codes` (`List[int]`): Retrieves a list of error codes.

#### `Error`

A class for defining error codes and messages.

##### Attributes:

- `code` (`int`): The error code.
- `message` (`str`): The error message.

#### `ResponseError`

A custom exception for response errors.

##### Attributes:

- `message` (`str`): The error message.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Angel Kürten  
Email: angel@angelkurten.com  
GitHub: [angelkurten](https://github.com/angelkurten/response_handler)
