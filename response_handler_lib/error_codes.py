from enum import Enum


class PredefinedErrorCodes(Enum):
    VALIDATION_ERROR = "VAL_ERR"
    NOT_FOUND = "NOT_FND"
    INTERNAL_ERROR = "INT_ERR"
    PERMISSION_DENIED = "PER_DEN"
    AUTHENTICATION_ERROR = "AUTH_ERR"
    REQUEST_TIMEOUT = "TIMEOUT"
    INVALID_REQUEST = "INV_REQ"
    BAD_REQUEST = "BAD_REQ"
    CONFLICT = "CONFLCT"
    FORBIDDEN = "FORBIDN"
    RESOURCE_GONE = "RES_GON"
    UNSUPPORTED_MEDIA_TYPE = "UNSUPMT"
    TOO_MANY_REQUESTS = "TOOMANY"
    SERVICE_UNAVAILABLE = "SVC_UNA"
    GATEWAY_TIMEOUT = "GATEWTO"
    BAD_GATEWAY = "BADGWAY"
    NOT_IMPLEMENTED = "NOT_IMP"
    PAYLOAD_TOO_LARGE = "PAY_TOL"
    URI_TOO_LONG = "URI_TOOL"
    UNSUPPORTED_OPERATION = "UNSUPP"
    DEPENDENCY_FAILED = "DEP_FAIL"
    NULL_POINTER = "NULLPTR"
    INDEX_OUT_OF_BOUNDS = "IDX_OOB"
    DIVISION_BY_ZERO = "DIV_ZERO"
    ILLEGAL_ARGUMENT = "ILL_ARG"
    ILLEGAL_STATE = "ILL_STA"
    TYPE_MISMATCH = "TYPEMIS"
    CONCURRENCY_ERROR = "CONCERR"
    DATA_INTEGRITY_VIOLATION = "DATINTV"
    RESOURCE_LEAK = "RES_LEK"
    INSUFFICIENT_FUNDS = "INS_FND"
    DUPLICATE_ENTRY = "DUP_ENT"
    EXCEEDS_LIMIT = "EXC_LIM"
    ITEM_UNAVAILABLE = "ITEM_UN"
    INVALID_COUPON = "INV_CPN"
    PROMOTION_EXPIRED = "PRO_EXP"
    ACCOUNT_LOCKED = "ACC_LCK"
    ACCOUNT_SUSPENDED = "ACC_SUS"
    UNAUTHORIZED_ACTION = "UNAUTH"
    INVALID_STATE_TRANSITION = "INV_STA"
    INSUFFICIENT_PRIVILEGES = "INS_PRI"
    DEPENDENCY_NOT_MET = "DEP_NOM"
    RATE_LIMIT_EXCEEDED = "RAT_LIM"
    OPERATION_FAILED = "OP_FAIL"
    SERVICE_DOWN = "SVC_DWN"
    INVALID_CONFIGURATION = "INV_CFG"
    POLICY_VIOLATION = "POL_VIO"
    SESSION_EXPIRED = "SES_EXP"
    QUOTA_EXCEEDED = "QUO_EXT"
    TRANSACTION_FAILED = "TRA_FAIL"
    UNSUPPORTED_VERSION = "UNS_VER"
    INVALID_FORMAT = "INV_FMT"
    RESOURCE_ALREADY_EXISTS = "RES_AEX"
    ACCESS_DENIED = "ACC_DEN"


ERROR_MESSAGES = {
    PredefinedErrorCodes.VALIDATION_ERROR.value: "Validation failed.",
    PredefinedErrorCodes.NOT_FOUND.value: "Resource not found.",
    PredefinedErrorCodes.INTERNAL_ERROR.value: "Internal server error.",
    PredefinedErrorCodes.PERMISSION_DENIED.value: "Permission denied.",
    PredefinedErrorCodes.AUTHENTICATION_ERROR.value: "Authentication error.",
    PredefinedErrorCodes.REQUEST_TIMEOUT.value: "Request timed out.",
    PredefinedErrorCodes.INVALID_REQUEST.value: "Invalid request.",
    PredefinedErrorCodes.BAD_REQUEST.value: "Bad request.",
    PredefinedErrorCodes.CONFLICT.value: "Conflict.",
    PredefinedErrorCodes.FORBIDDEN.value: "Forbidden.",
    PredefinedErrorCodes.RESOURCE_GONE.value: "Resource gone.",
    PredefinedErrorCodes.UNSUPPORTED_MEDIA_TYPE.value: "Unsupported media type.",
    PredefinedErrorCodes.TOO_MANY_REQUESTS.value: "Too many requests.",
    PredefinedErrorCodes.SERVICE_UNAVAILABLE.value: "Service unavailable.",
    PredefinedErrorCodes.GATEWAY_TIMEOUT.value: "Gateway timeout.",
    PredefinedErrorCodes.BAD_GATEWAY.value: "Bad gateway.",
    PredefinedErrorCodes.NOT_IMPLEMENTED.value: "Not implemented.",
    PredefinedErrorCodes.PAYLOAD_TOO_LARGE.value: "Payload too large.",
    PredefinedErrorCodes.URI_TOO_LONG.value: "URI too long.",
    PredefinedErrorCodes.UNSUPPORTED_OPERATION.value: "Operation not supported.",
    PredefinedErrorCodes.DEPENDENCY_FAILED.value: "Dependency failed.",
    PredefinedErrorCodes.NULL_POINTER.value: "Null pointer error.",
    PredefinedErrorCodes.INDEX_OUT_OF_BOUNDS.value: "Index out of bounds.",
    PredefinedErrorCodes.DIVISION_BY_ZERO.value: "Division by zero.",
    PredefinedErrorCodes.ILLEGAL_ARGUMENT.value: "Illegal argument.",
    PredefinedErrorCodes.ILLEGAL_STATE.value: "Illegal state.",
    PredefinedErrorCodes.TYPE_MISMATCH.value: "Type mismatch.",
    PredefinedErrorCodes.CONCURRENCY_ERROR.value: "Concurrency error.",
    PredefinedErrorCodes.DATA_INTEGRITY_VIOLATION.value: "Data integrity violation.",
    PredefinedErrorCodes.RESOURCE_LEAK.value: "Resource leak detected.",
    PredefinedErrorCodes.INSUFFICIENT_FUNDS.value: "Insufficient funds.",
    PredefinedErrorCodes.DUPLICATE_ENTRY.value: "Duplicate entry.",
    PredefinedErrorCodes.EXCEEDS_LIMIT.value: "Exceeds allowable limit.",
    PredefinedErrorCodes.ITEM_UNAVAILABLE.value: "Item unavailable.",
    PredefinedErrorCodes.INVALID_COUPON.value: "Invalid coupon code.",
    PredefinedErrorCodes.PROMOTION_EXPIRED.value: "Promotion expired.",
    PredefinedErrorCodes.ACCOUNT_LOCKED.value: "Account is locked.",
    PredefinedErrorCodes.ACCOUNT_SUSPENDED.value: "Account is suspended.",
    PredefinedErrorCodes.UNAUTHORIZED_ACTION.value: "Unauthorized action.",
    PredefinedErrorCodes.INVALID_STATE_TRANSITION.value: "Invalid state transition.",
    PredefinedErrorCodes.INSUFFICIENT_PRIVILEGES.value: "Insufficient privileges.",
    PredefinedErrorCodes.DEPENDENCY_NOT_MET.value: "Dependency not met.",
    PredefinedErrorCodes.RATE_LIMIT_EXCEEDED.value: "Rate limit exceeded.",
    PredefinedErrorCodes.OPERATION_FAILED.value: "Operation failed.",
    PredefinedErrorCodes.SERVICE_DOWN.value: "Service is currently down.",
    PredefinedErrorCodes.INVALID_CONFIGURATION.value: "Invalid configuration.",
    PredefinedErrorCodes.POLICY_VIOLATION.value: "Policy violation.",
    PredefinedErrorCodes.SESSION_EXPIRED.value: "Session expired.",
    PredefinedErrorCodes.QUOTA_EXCEEDED.value: "Quota exceeded.",
    PredefinedErrorCodes.TRANSACTION_FAILED.value: "Transaction failed.",
    PredefinedErrorCodes.UNSUPPORTED_VERSION.value: "Unsupported version.",
    PredefinedErrorCodes.INVALID_FORMAT.value: "Invalid format.",
    PredefinedErrorCodes.RESOURCE_ALREADY_EXISTS.value: "Resource already exists.",
    PredefinedErrorCodes.ACCESS_DENIED.value: "Access denied."
}
