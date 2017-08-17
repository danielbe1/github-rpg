class GithubWebhookHandlerException(Exception):
    '''
    The base class for all github webhook errors.
    '''

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class GithubWebhookMalformedEventError(GithubWebhookHandlerException):
    '''
    Thrown when the webhook event is not valid; e.g., missing fields in the event JSON.
    '''

    def __init__(self, event, description):
        GithubWebhookHandlerException.__init__(self, f'malformed {event} event: {description}')


class GithubWebhookBadRequestError(GithubWebhookHandlerException):
    '''
    Thrown when the webhook request is not valid for any reason; e.g., missing headers.
    '''
    def __init__(self, description):
        GithubWebhookHandlerException.__init__(self, description)