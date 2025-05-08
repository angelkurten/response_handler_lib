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
- **HTTP Interceptor**: Built-in HTTP request handling with automatic error mapping
- **Detailed Error Information**: Support for additional error context and where information
- **Python 3.8+ Support**: Compatible with Python versions 3.8 through 3.12

## Installation

```bash
pip install response_handler_lib
```

## Quick Start

```python
from response_handler_lib import Response, Either, Success, Failure, ErrorItem
from response_handler_lib.http_interceptor import HTTPInterceptor

# Create a successful response
response = Response(data={"message": "Hello, World!"})
print(response.to_json())
# Output: {"data": {"message": "Hello, World!"}, "errors": [], "context": {}, "status_code": 200}

# Create a response with an error
error = ErrorItem.create("VAL_ERROR", "Invalid input", "The input value was invalid")
response = Response(errors=[error])
print(response.to_json())
# Output: {"data": null, "errors": [{"code": "VAL_ERROR", "message": "Invalid input", "where": "The input value was invalid"}], "context": {}, "status_code": 400}

# Use Either for functional error handling
def process_data(data):
    if not data:
        return Failure([ErrorItem.create("VAL_ERROR", "Data is required", "No data provided")])
    return Success({"processed": data})

# Convert Either to Response
either = process_data(None)
response = Response.from_either(either)
print(response.to_json())
# Output: {"data": null, "errors": [{"code": "VAL_ERROR", "message": "Data is required", "where": "No data provided"}], "context": {}, "status_code": 400}

# Use HTTP Interceptor for making requests
interceptor = HTTPInterceptor()
response = interceptor.request('GET', 'https://api.example.com/data')
print(response.to_json())
```

## Real-World Examples

### User Registration Validation

```python
def validate_user_registration(email: str, password: str, username: str) -> Either[List[ErrorItem], Dict]:
    errors = []
    
    # Validate email
    if '@' not in email:
        errors.append(ErrorItem.create(
            "INVALID_EMAIL",
            "The email format is not valid",
            f"Invalid email format: {email}"
        ))
    
    # Validate password
    if len(password) < 8:
        errors.append(ErrorItem.create(
            "PASSWORD_TOO_SHORT",
            "Password must be at least 8 characters long",
            f"Password length: {len(password)}"
        ))
    
    if errors:
        return Failure(errors)
    
    return Success({
        "email": email,
        "username": username,
        "status": "registered"
    })
```

### Payment Processing

```python
def process_payment(amount: float, currency: str) -> Either[ErrorItem, Dict]:
    if amount <= 0:
        return Failure(ErrorItem.create(
            "INVALID_AMOUNT",
            "Amount must be greater than zero",
            f"The amount is {amount}"
        ))
    
    valid_currencies = ["USD", "EUR", "MXN"]
    if currency not in valid_currencies:
        return Failure(ErrorItem.create(
            "INVALID_CURRENCY",
            f"Unsupported currency. Valid currencies are: {', '.join(valid_currencies)}",
            f"Provided currency: {currency}"
        ))
    
    return Success({
        "transaction_id": "TXN123456",
        "amount": amount,
        "currency": currency,
        "status": "completed"
    })
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

## Advanced Features

### Success.of() Factory Method

The library provides a factory method for creating Success instances with explicit type information:

```python
from response_handler_lib import Success

# Create a Success instance with explicit type
success = Success.of({"key": "value"})  # Type: Success[L, Dict[str, str]]
```

### Customizable JSON Output

The library allows you to customize the JSON output by controlling which fields are included:

```python
from response_handler_lib import Config, Response

# Disable context in JSON output
Config.ENABLE_CONTEXT_IN_JSON = False

# Disable 'where' field in error output
Config.ENABLE_WHERE_IN_JSON = False

# Create a response
response = Response(data={"key": "value"})
print(response.to_json())  # Context and where fields will be excluded
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
