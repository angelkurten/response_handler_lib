from enum import Enum


class PredefinedErrorCodes(Enum):
    VALIDATION_ERROR = "VAL_001"
    NOT_FOUND = "NOT_002"
    INTERNAL_ERROR = "INT_003"
    PERMISSION_DENIED = "PER_004"
    AUTHENTICATION_ERROR = "AUT_005"
    REQUEST_TIMEOUT = "TIM_006"
    INVALID_REQUEST = "INV_007"
    BAD_REQUEST = "BAD_008"
    CONFLICT = "CON_009"
    FORBIDDEN = "FOR_010"
    RESOURCE_GONE = "GON_011"
    UNSUPPORTED_MEDIA_TYPE = "UMT_012"
    TOO_MANY_REQUESTS = "TMR_013"
    SERVICE_UNAVAILABLE = "SUA_014"
    GATEWAY_TIMEOUT = "GWT_015"
    BAD_GATEWAY = "BGW_016"
    NOT_IMPLEMENTED = "NIM_017"
    PAYLOAD_TOO_LARGE = "PTL_018"
    URI_TOO_LONG = "UTL_019"
    UNSUPPORTED_OPERATION = "UOP_020"
    DEPENDENCY_FAILED = "DEF_021"
    NULL_POINTER = "NUL_022"
    INDEX_OUT_OF_BOUNDS = "IOB_023"
    DIVISION_BY_ZERO = "DBZ_024"
    ILLEGAL_ARGUMENT = "IAR_025"
    ILLEGAL_STATE = "IST_026"
    TYPE_MISMATCH = "TYP_027"
    CONCURRENCY_ERROR = "CON_028"
    DATA_INTEGRITY_VIOLATION = "DIV_029"
    RESOURCE_LEAK = "REL_030"
    INSUFFICIENT_FUNDS = "INF_031"
    DUPLICATE_ENTRY = "DUP_032"
    EXCEEDS_LIMIT = "EXL_033"
    ITEM_UNAVAILABLE = "ITU_034"
    INVALID_COUPON = "ICP_035"
    PROMOTION_EXPIRED = "PEX_036"
    ACCOUNT_LOCKED = "ACL_037"
    ACCOUNT_SUSPENDED = "ACS_038"
    UNAUTHORIZED_ACTION = "UNA_039"
    INVALID_STATE_TRANSITION = "IST_040"
    INSUFFICIENT_PRIVILEGES = "INP_041"
    DEPENDENCY_NOT_MET = "DNM_042"
    RATE_LIMIT_EXCEEDED = "RLE_043"
    OPERATION_FAILED = "OPF_044"
    SERVICE_DOWN = "SDN_045"
    INVALID_CONFIGURATION = "ICF_046"
    POLICY_VIOLATION = "POV_047"
    SESSION_EXPIRED = "SEX_048"
    QUOTA_EXCEEDED = "QEX_049"
    TRANSACTION_FAILED = "TRF_050"
    UNSUPPORTED_VERSION = "USV_051"
    INVALID_FORMAT = "IFM_052"
    RESOURCE_ALREADY_EXISTS = "RAE_053"
    ACCESS_DENIED = "ACD_054"


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
