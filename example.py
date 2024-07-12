from response_handler_lib.errors import ErrorResponseConfig
from response_handler_lib.response import Response


class Example:
    response = Response()

    def __init__(self):
        custom_errors = {
            "CUS_ERR1": "Custom error message 1.",
            "CUS_ERR2": "Custom error message 2."
        }
        ErrorResponseConfig.add_custom_errors(custom_errors)

    def test(self):
        self.response.add_error("VAL_ERR")
        self.response.add_error("CUS_ERR1")
        return self.response.to_json(include_where=True)


print(Example().test())