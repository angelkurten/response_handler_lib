# Response Handler Library

A Python library for handling responses and errors in a consistent way.

## Overview

This library provides a set of tools for handling responses and errors in a consistent way across your application. It includes:

- `Either` monad for intermediate error handling
- `Response` class for final response formatting
- `ErrorItem` for error representation
- Predefined error codes and messages

## Installation

```bash
pip install response_handler_lib
```

## Usage

### Error Handling with Either

The `Either` monad is used for intermediate error handling in your business logic:

```python
from response_handler_lib.either import Either, Success, Failure, ErrorItem

def process_data(data: dict) -> Either:
    if not data.get("required_field"):
        return Failure([
            ErrorItem.create(
                code="VAL_MISSING_FIELD",
                message="Required field is missing",
                context={"field": "required_field"}
            )
        ])
    return Success(processed_data)
```

### Final Response Formatting

The `Response` class is used to format the final output:

```python
from response_handler_lib.response import Response
from response_handler_lib.either import Either

# Convert from Either to Response
either = process_data(data)
response = Response.from_either(either)

# Get the response as a dictionary
result = response.to_dict()
# {
#     "status_code": 400,
#     "data": null,
#     "errors": [
#         {
#             "code": "VAL_MISSING_FIELD",
#             "message": "Required field is missing",
#             "where": "file.py, process_data, line 10"
#         }
#     ],
#     "context": {
#         "field": "required_field"
#     }
# }

# Get the response as JSON
json_response = response.to_json()
```

## API Reference

### Either

- `Success(value)`: Creates a successful result
- `Failure(errors)`: Creates a failed result with errors
- `ErrorItem.create(code, message, where=None, context=None)`: Creates an error item

### Response

- `Response(data=None, errors=None, context=None, status_code=200)`: Creates a response
- `Response.from_either(either)`: Creates a response from an Either
- `to_dict(include_where=False)`: Converts the response to a dictionary
- `to_json(include_where=False)`: Converts the response to a JSON string

## License

MIT

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/response-handler](https://github.com/yourusername/response-handler)
