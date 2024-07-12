# response_handler_lib

[![Coverage Status](https://coveralls.io/repos/github/angelkurten/response_handler/badge.svg?branch=main)](https://coveralls.io/github/angelkurten/response_handler?branch=main)

A package for handling responses with potential errors and generic data, including predefined and custom error handling. This package is used as a complement to exceptions to have more control over business logic errors.

## Features

- Custom `Response` class for handling responses with errors and data.
- Custom `ErrorResponse` class for defining error codes and messages.
- `ErrorResponseConfig` class for managing predefined and custom error configurations.
- `PredefinedErrorCodes` enum for predefined error codes.
- Utilities for adding errors, checking for errors, and retrieving error messages and codes.
- HTTP Interceptor class for handling HTTP requests and responses with built-in error handling.
- Convert `Response` to JSON format.
- Customizable logger for error reporting.
- Add context information to responses.
- Enable or disable context and error location (`where`) in JSON output.

## Installation

You can install `response_handler_lib` via pip:

```sh
pip install response_handler_lib
```

## Usage

### Importing the Package

To use the `Response` class and related utilities, import them from the `response_handler_lib` package:

```python
from response_handler_lib import Response, ErrorResponseConfig, PredefinedErrorCodes
```

### Configuring the Package

You can configure various aspects of the package, such as logger:

```python
# Configure a custom logger
custom_logger = logging.getLogger("custom_logger")
custom_logger.setLevel(logging.DEBUG)
config.configure_logger(custom_logger)

# Enable or disable logging
config.enable_logs(True)  # Enable logging
config.enable_logs(False)  # Disable logging

# Enable or disable context in JSON output
config.enable_context_in_json(True)  # Enable context
config.enable_context_in_json(False)  # Disable context

# Enable or disable error location (`where`) in JSON output
config.enable_where_in_json(True)  # Enable where
config.enable_where_in_json(False)  # Disable where
```

### Creating a Successful Response

Create a `Response` object and provide any data:

```python
response = Response(data="Some data")
if not response.has_errors:
    print("Response is successful")
    print("Data:", response.data)
```

### Adding Context to a Response

Add context information to a `Response` object:

```python
response = Response(data="Some data")
response.add_context("user", {"id": 1, "name": "John Doe"})
print(response.to_json())
```

### Creating a Failed Response with Predefined Errors

Add predefined errors to a response using the `add_error` method:

```python
response = Response()
response.add_error(PredefinedErrorCodes.VAL_ERR.value)
response.add_error(PredefinedErrorCodes.NOT_FND.value)

if response.has_errors:
    print("Errors:")
    for code, message in zip(response.error_types, response.error_messages):
        print(f"Error {code}: {message}")
```

### Adding Custom Errors to the Configuration

Add custom errors to the `ErrorResponseConfig`:

```python
ErrorResponseConfig.add_custom_error("CUS_ERR1", "Custom error message 1.")
ErrorResponseConfig.add_custom_error("CUS_ERR2", "Custom error message 2.")
```

### Creating a Failed Response with Custom Errors

Add custom errors to a response using the `add_error` method:

```python
response = Response()
response.add_error("CUS_ERR1")
response.add_error("CUS_ERR2")

if response.has_errors:
    print("Errors:")
    for code, message in zip(response.error_types, response.error_messages):
        print(f"Error {code}: {message}")
```

### Adding Multiple Custom Errors at Once

Add multiple custom errors to the `ErrorResponseConfig`:

```python
custom_errors = {
    "CUS_ERR3": "Custom error message 3.",
    "CUS_ERR4": "Custom error message 4."
}

ErrorResponseConfig.add_custom_errors(custom_errors)
```

### Handling Undefined Errors

Attempting to add an undefined error raises a `ValueError`:

```python
response = Response()

try:
    response.add_error("NOT_DEFINED")
except ValueError as e:
    print("Caught an error:", str(e))
```

### Converting a Response to JSON

Convert a `Response` object to JSON format using the `to_json` method:

```python
response = Response(data="Some data")
response.add_error("VAL_ERR")
print(response.to_json())
```

### Including `where` in the JSON Output

Convert a `Response` object to JSON format, optionally including the `where` property:

```python
response = Response(data="Some data")
response.add_error("VAL_ERR")
print(response.to_json(include_where=True))
```
### Using the HTTPInterceptor

The `HTTPInterceptor` class is designed to handle HTTP requests and responses with built-in error handling. Here is how to use it:

```python
interceptor = HTTPInterceptor()

# Successful GET request
response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
print(response_json)

# Handling a 404 Not Found error
response_json = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/invalid-endpoint')
print(response_json)

```


## API Reference

### Classes

#### `Response`

A generic class for handling responses.

##### Attributes:

- `errors` (`Optional[List[ErrorResponse]]`): A list of errors in the response.
- `data` (`Optional[T]`): The data in the response.
- `context` (`Optional[Dict[str, Any]]`): Additional context information.

##### Methods:

- `add_error(error_code: str)`: Adds an error to the response.
- `has_errors` (`bool`): Checks if the response has errors.
- `error_messages` (`List[str]`): Retrieves a list of error messages.
- `error_types` (`List[str]`): Retrieves a list of error codes.
- `to_json(include_where: bool = False)`: Converts the response to JSON format, optionally including the `where` property.
- `add_context(key: str, value: Any)`: Adds context information to the response.

#### `ErrorResponse`

A class for defining error codes and messages.

##### Attributes:

- `code` (`str`): The error code.
- `message` (`str`): The error message.
- `where` (`Optional[str]`): The location where the error was generated.

#### `ErrorResponseConfig`

A class for managing predefined and custom error configurations.

##### Methods:

- `add_custom_error(code: str, message: str)`: Adds a custom error to the configuration.
- `add_custom_errors(errors: Dict[str, str])`: Adds multiple custom errors to the configuration.
- `get_error(code: str)`: Retrieves an error by code.

#### `PredefinedErrorCodes`

An enum for predefined error codes.

#### HTTPInterceptor

A class for handling HTTP requests and responses with built-in error handling.

##### Methods:

- `request(method: str, url: str, **kwargs)`: Sends an HTTP request and returns the response JSON.
- `handle_http_error(http_err: HTTPError, resp)`: Handles HTTP errors based on status code.
- `handle_generic_error(err: Exception)`: Handles generic errors.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Angel Kürten  
Email: angel@angelkurten.com  
GitHub: [angelkurten](https://github.com/angelkurten/response_handler)
