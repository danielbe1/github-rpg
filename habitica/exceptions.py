class HabiticaCLientException(Exception):
    '''
    The base class for all habitica API client errors.
    '''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class HabiticaCLientConfigError(HabiticaCLientException):
    '''
    Thrown if configuration for the habitica API client is missing or invalid.
    '''
    def __init__(self, description):
        HabiticaCLientException.__init__(self, description)


class HabiticaCLientConnectivityError(HabiticaCLientException):
    '''
    The base class for all habitica API client connectivity errors; e.g., request timeouts.
    '''
    def __init__(self, description):
        HabiticaCLientException.__init__(self, description)


class HabiticaClientTimeoutError(HabiticaCLientConnectivityError):
    '''
    Thrown when API calls timeout.
    '''
    def __init__(self):
        HabiticaCLientConnectivityError.__init__(self, 'habitica API request timed out')


class HabiticaClientIllegalResponseError(HabiticaCLientConnectivityError):
    '''
    Thrown when the response to an API call cannot be validated as an API response; e.g., the body is not a JSON.
    '''
    def __init__(self):
        HabiticaCLientConnectivityError.__init__(self, f'illegal response')


class HabiticaClientAPIError(HabiticaCLientException):
    '''
    The base class for API logical and validation errors.
    '''
    def __init__(self, description):
        HabiticaCLientException.__init__(self, description)


class HabiticaClientHttpStatusCodeError(HabiticaCLientException):
    '''
    Thrown when the status code returned after an API call is unexpected.

    Note that 4xx errors are not always unexpected and that 2xx status codes are not always expected,
    it depends on the speicifc API call itself.
    '''
    def __init__(self, status_code, body):
        HabiticaCLientException.__init__(self, f'unexpected status code: {status_code}: {body}')

        self.status_code = status_code


class HabiticaClientAPIUnauthorizedError(HabiticaClientAPIError):
    '''
    Thrown when the credentials (user and api keys) are missing or invalid.
    '''
    def __init__(self, description):
        HabiticaCLientConnectivityError.__init__(self, f'unauthorized action: {description}')


class HabiticaClientAPIMalformedObjectError(HabiticaClientAPIError):
    '''
    Thrown when an API object is invalid; e.g., missing fields in object JSON.
    '''
    def __init__(self, obj, description):
        HabiticaCLientConnectivityError.__init__(self, f'malformed {obj} object: {description}')
