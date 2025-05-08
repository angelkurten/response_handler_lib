from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.either import Either, ErrorItem, Success, Failure
from response_handler_lib.http_interceptor import HTTPInterceptor
import json
from typing import List


class Example:
    def __init__(self):
        # Define custom error messages
        self.custom_errors = {
            "CUS_ERR1": "Custom error message 1.",
            "CUS_ERR2": "Custom error message 2."
        }
        self.interceptor = HTTPInterceptor()

    def generate_success_response(self) -> Either[ErrorItem, str]:
        return Success("This is a successful response.")

    def generate_error_response(self) -> Either[List[ErrorItem], None]:
        errors = [
            ErrorItem.create(PredefinedErrorCodes.VALIDATION_ERROR, "Validation failed: Invalid input"),
            ErrorItem.create(PredefinedErrorCodes.AUTHENTICATION_ERROR, "Authentication failed: Invalid credentials")
        ]
        return Failure(errors)

    def generate_mixed_response(self) -> Either[ErrorItem, str]:
        # In a real application, you would typically return either success or error
        # This is just for demonstration purposes
        return Success("This response has data.")

    def get_user_by_id(self, user_id: str) -> Either[ErrorItem, dict]:
        if user_id == "123":
            return Success({
                "id": "123",
                "name": "Alice"
            })
        return Failure(ErrorItem.create("USER_NOT_FOUND", "El usuario no existe"))

    def print_responses(self):
        # Generate and print a successful response
        success_response = self.generate_success_response()
        print("---- Success Response ----")
        print(json.dumps(json.loads(success_response.to_json()), indent=4))
        print("\n")

        # Generate and print an error response
        error_response = self.generate_error_response()
        print("---- Error Response ----")
        print(json.dumps(json.loads(error_response.to_json(include_where=True)), indent=4))
        print("\n")

        # Generate and print a mixed response
        mixed_response = self.generate_mixed_response()
        print("---- Mixed Response ----")
        print(json.dumps(json.loads(mixed_response.to_json()), indent=4))
        print("\n")

        # Test get_user_by_id
        user_found = self.get_user_by_id("123")
        print("---- User Found Response ----")
        print(json.dumps(json.loads(user_found.to_json()), indent=4))
        print("\n")

        user_not_found = self.get_user_by_id("456")
        print("---- User Not Found Response ----")
        print(json.dumps(json.loads(user_not_found.to_json(include_where=True)), indent=4))
        print("\n")


# Run the example
example = Example()
example.print_responses()

# Test HTTP Interceptor with different status codes
interceptor = HTTPInterceptor()

# Test successful request
response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
print("---- HTTP Interceptor Success Response ----")
print(json.dumps(json.loads(response.to_json()), indent=4))
print("\n")

# Test 404 error
response = interceptor.request('GET', 'https://example.com/404')
print("---- HTTP Interceptor 404 Error Response ----")
print(json.dumps(json.loads(response.to_json()), indent=4))
print("\n")

# Test 401 error
response = interceptor.request('GET', 'https://httpstat.us/401')
print("---- HTTP Interceptor 401 Error Response ----")
print(json.dumps(json.loads(response.to_json()), indent=4))
print("\n")

# Test 403 error
response = interceptor.request('GET', 'https://httpstat.us/403')
print("---- HTTP Interceptor 403 Error Response ----")
print(json.dumps(json.loads(response.to_json()), indent=4))
print("\n")
