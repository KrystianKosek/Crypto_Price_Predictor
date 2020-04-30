error_codes_mapping = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}


class RequestError(Exception):
    """Base class for errors"""
    pass


class RequestCodeError(RequestError):
    """Raised when request status code is >= 400"""
    def __init__(self, message, error_code):
        super().__init__(message + "\n %s" % ' '.join((str(error_code), error_codes_mapping.get(error_code))))