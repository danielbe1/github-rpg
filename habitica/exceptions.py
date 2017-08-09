class HabiticaCLientException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class HabiticaCLientConnectivityError(HabiticaCLientException):
    def __init__(self, description):
        HabiticaCLientException.__init__(self, description)


class HabiticaClientTimeoutError(HabiticaCLientConnectivityError):
    def __init__(self):
        HabiticaCLientConnectivityError.__init__(self, 'habitica API request timed out')


class HabiticaClientHttpStatusCodeError(HabiticaCLientConnectivityError):
    def __init__(self, status_code, body):
        HabiticaCLientConnectivityError.__init__(self, f'unexpected status code: {status_code}: {body}')

        self.status_code = status_code


class HabiticaClientIllegalResponseError(HabiticaCLientConnectivityError):
    def __init__(self):
        HabiticaCLientConnectivityError.__init__(self, f'illegal response')


class HabiticaClientAPIError(HabiticaCLientException):
    def __init__(self, message):
        HabiticaCLientConnectivityError.__init__(self, message)


class HabiticaClientAPIUnauthorizedError(HabiticaClientAPIError):
    def __init__(self, message):
        HabiticaCLientConnectivityError.__init__(self, f'unauthorized action: {message}')


class HabiticaClientAPIMalformedObjectError(HabiticaClientAPIError):
    def __init__(self, object, message):
        HabiticaCLientConnectivityError.__init__(self, f'malformed {object} object: {message}')