class GithubWebhookHandlerException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class GithubWebhookMalformedEventError(GithubWebhookHandlerException):
    def __init__(self, event, description):
        GithubWebhookHandlerException.__init__(self, f'malformed {event} event: {description}')


class GithubWebhookBadRequestError(GithubWebhookHandlerException):
    def __init__(self, description):
        GithubWebhookHandlerException.__init__(self, description)