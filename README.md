# Response Handler

[![Coverage Status](https://coveralls.io/repos/github/angelkurten/response_handler/badge.svg?branch=main)](https://coveralls.io/github/angelkurten/response_handler?branch=main)
![PyPI - Downloads](https://img.shields.io/pypi/dm/response_handler_lib)

A Python library for handling HTTP responses and error management in a consistent and type-safe way.

## Features

- **Type-safe Response Handling**: Built with Pydantic for robust data validation and serialization
- **Either Pattern**: Functional error handling with `Either` type for success/failure cases
- **HTTP Status Code Management**: Automatic status code mapping based on error types
- **Context Support**: Add contextual information to responses and errors
- **JSON Serialization**: Built-in JSON serialization with customizable output
- **OpenAPI/Swagger Support**: Automatic schema generation for API documentation

## Installation

```bash
pip install response_handler_lib
```

## Quick Start

```python
from response_handler_lib import Response, Either, Success, Failure, ErrorItem

# Create a successful response
response = Response(data={"message": "Hello, World!"})
print(response.to_json())
# Output: {"data": {"message": "Hello, World!"}, "errors": [], "context": {}, "status_code": 200}

# Create a response with an error
error = ErrorItem.create("VAL_ERROR", "Invalid input")
response = Response(errors=[error])
print(response.to_json())
# Output: {"data": null, "errors": [{"code": "VAL_ERROR", "message": "Invalid input", "where": null}], "context": {}, "status_code": 400}

# Use Either for functional error handling
def process_data(data):
    if not data:
        return Failure([ErrorItem.create("VAL_ERROR", "Data is required")])
    return Success({"processed": data})

# Convert Either to Response
either = process_data(None)
response = Response.from_either(either)
print(response.to_json())
# Output: {"data": null, "errors": [{"code": "VAL_ERROR", "message": "Data is required", "where": null}], "context": {}, "status_code": 400}
```

## Error Types and Status Codes

The library automatically maps error types to appropriate HTTP status codes:

- `VAL_ERROR` → 400 (Bad Request)
- `AUTH_ERROR` → 401 (Unauthorized)
- `FORB_ERROR` → 403 (Forbidden)
- `NOT_ERROR` → 404 (Not Found)
- `TIM_ERROR` → 408 (Request Timeout)
- `INT_ERROR` → 500 (Internal Server Error)

## Configuration

```python
from response_handler_lib import Config

# Enable context in JSON output
Config.ENABLE_CONTEXT_IN_JSON = True

# Enable 'where' field in error output
Config.ENABLE_WHERE_IN_JSON = True

# Enable logging
Config.ENABLE_LOGS = True
```

## Pydantic Integration

The library uses Pydantic for data validation and serialization. This provides:

- Automatic data validation
- Type checking
- JSON schema generation
- OpenAPI/Swagger integration
- Efficient serialization/deserialization

Example of Pydantic features:

```python
from response_handler_lib import Response
from pydantic import ValidationError

# Automatic validation
try:
    response = Response(status_code=999)  # Will raise ValidationError
except ValidationError as e:
    print(e)

# JSON schema generation
print(Response.model_json_schema())
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Angel Kürten  
Email: angel@angelkurten.com  
GitHub: [angelkurten](https://github.com/angelkurten/response_handler)
