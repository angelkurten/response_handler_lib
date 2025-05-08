from response_handler_lib.error_codes import PredefinedErrorCodes
from response_handler_lib.either import Either, ErrorItem, Success, Failure
from response_handler_lib.http_interceptor import HTTPInterceptor
import json
from typing import List, Dict, Optional


class Example:
    """
    Example class that demonstrates the usage of the response_handler_lib library.
    Includes examples of handling successful responses and errors.
    """
    def __init__(self):
        # Custom error messages definition
        self.custom_errors: Dict[str, str] = {
            "INVALID_EMAIL": "The email format is not valid",
            "PASSWORD_TOO_SHORT": "Password must be at least 8 characters long",
            "USERNAME_TAKEN": "Username is already taken"
        }
        self.interceptor = HTTPInterceptor()

    def validate_user_registration(self, email: str, password: str, username: str) -> Either[List[ErrorItem], Dict]:
        """
        Example of user registration validation.
        
        Args:
            email: User's email address
            password: User's password
            username: User's username
            
        Returns:
            Either[List[ErrorItem], Dict]: List of errors or user data
        """
        errors = []
        
        # Validate email
        if '@' not in email:
            errors.append(ErrorItem.create("INVALID_EMAIL", self.custom_errors["INVALID_EMAIL"]))
        
        # Validate password
        if len(password) < 8:
            errors.append(ErrorItem.create("PASSWORD_TOO_SHORT", self.custom_errors["PASSWORD_TOO_SHORT"]))
        
        # If there are errors, return Failure
        if errors:
            return Failure(errors)
        
        # If everything is fine, return Success with user data
        return Success({
            "email": email,
            "username": username,
            "status": "registered"
        })

    def get_user_profile(self, user_id: str) -> Either[ErrorItem, Dict]:
        """
        Example of user profile retrieval.
        
        Args:
            user_id: User's ID
            
        Returns:
            Either[ErrorItem, Dict]: Error or profile data
        """
        # Simulated users database
        users_db = {
            "123": {
                "id": "123",
                "name": "John Doe",
                "email": "john@example.com",
                "role": "admin"
            },
            "456": {
                "id": "456",
                "name": "Jane Smith",
                "email": "jane@example.com",
                "role": "user"
            }
        }
        
        if user_id in users_db:
            return Success(users_db[user_id])
        
        return Failure(ErrorItem.create(
            "USER_NOT_FOUND",
            f"No user found with ID: {user_id}"
        ))

    def process_payment(self, amount: float, currency: str) -> Either[ErrorItem, Dict]:
        """
        Example of payment processing.
        
        Args:
            amount: Payment amount
            currency: Payment currency
            
        Returns:
            Either[ErrorItem, Dict]: Error or payment confirmation
        """
        # Validate amount
        if amount <= 0:
            return Failure(ErrorItem.create(
                "INVALID_AMOUNT",
                "Amount must be greater than zero",
                f"The amount is {amount}"
            ))
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "MXN"]
        if currency not in valid_currencies:
            return Failure(ErrorItem.create(
                "INVALID_CURRENCY",
                f"Unsupported currency. Valid currencies are: {', '.join(valid_currencies)}"
            ))
        
        # Simulate successful processing
        return Success({
            "transaction_id": "TXN123456",
            "amount": amount,
            "currency": currency,
            "status": "completed",
            "timestamp": "2024-03-20T10:30:00Z"
        })

    def print_examples(self):
        """
        Prints examples of using different methods.
        """
        # Registration validation example
        print("\n=== Registration Validation Example ===")
        # Error case
        invalid_registration = self.validate_user_registration(
            email="invalid-email",
            password="123",
            username="john"
        )
        print("Invalid registration:")
        print(json.dumps(json.loads(invalid_registration.to_json(include_where=True)), indent=4))
        
        # Success case
        valid_registration = self.validate_user_registration(
            email="john@example.com",
            password="secure123",
            username="john"
        )
        print("\nValid registration:")
        print(json.dumps(json.loads(valid_registration.to_json()), indent=4))

        # User profile retrieval example
        print("\n=== User Profile Retrieval Example ===")
        # Existing user
        existing_user = self.get_user_profile("123")
        print("User found:")
        print(json.dumps(json.loads(existing_user.to_json()), indent=4))
        
        # Non-existing user
        non_existing_user = self.get_user_profile("999")
        print("\nUser not found:")
        print(json.dumps(json.loads(non_existing_user.to_json(include_where=True)), indent=4))

        # Payment processing example
        print("\n=== Payment Processing Example ===")
        # Valid payment
        valid_payment = self.process_payment(100.50, "USD")
        print("Successful payment:")
        print(json.dumps(json.loads(valid_payment.to_json()), indent=4))
        
        # Invalid payment
        invalid_payment = self.process_payment(-50, "XYZ")
        print("\nFailed payment:")
        print(json.dumps(json.loads(invalid_payment.to_json(include_where=True)), indent=4))


# Run examples
if __name__ == "__main__":
    example = Example()
    example.print_examples()

    # HTTP Interceptor examples
    print("\n=== HTTP Interceptor Examples ===")
    interceptor = HTTPInterceptor()

    # Successful request example
    print("\nSuccessful request:")
    response = interceptor.request('GET', 'https://jsonplaceholder.typicode.com/posts/1')
    print(json.dumps(json.loads(response.to_json()), indent=4))

    # 404 error example
    print("\n404 error:")
    response = interceptor.request('GET', 'https://example.com/404')
    print(json.dumps(json.loads(response.to_json()), indent=4))

    # 401 error example
    print("\n401 error:")
    response = interceptor.request('GET', 'https://httpstat.us/401')
    print(json.dumps(json.loads(response.to_json()), indent=4))
