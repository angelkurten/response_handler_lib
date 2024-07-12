
# response_handler_lib

A package for handling responses with potential errors and generic data, including predefined and custom error handling. This package is used as a complement to exceptions to have more control over business logic errors.

## Features

- Custom `Response` class for handling responses with errors and data.
- Custom `ErrorResponse` class for defining error codes and messages.
- `ErrorResponseConfig` class for managing predefined and custom error configurations.
- `PredefinedErrorCodes` enum for predefined error codes.
- Utilities for adding errors, checking for errors, and retrieving error messages and codes.
- Convert `Response` to JSON format.

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

### Creating a Successful Response

Create a `Response` object and provide any data:

```python
response = Response(data="Some data")
if not response.has_errors:
    print("Response is successful")
    print("Data:", response.data)
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

## API Reference

### Classes

#### `Response`

A generic class for handling responses.

##### Attributes:

- `errors` (`Optional[List[ErrorResponse]]`): A list of errors in the response.
- `data` (`Optional[T]`): The data in the response.

##### Methods:

- `add_error(error_code: str)`: Adds an error to the response.
- `has_errors` (`bool`): Checks if the response has errors.
- `error_messages` (`List[str]`): Retrieves a list of error messages.
- `error_types` (`List[str]`): Retrieves a list of error codes.
- `to_json(include_where: bool = False)`: Converts the response to JSON format, optionally including the `where` property.

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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Angel Kürten  
Email: angel@angelkurten.com  
GitHub: [angelkurten](https://github.com/angelkurten/response_handler)
