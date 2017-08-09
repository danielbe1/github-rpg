from github.exceptions import GithubWebhookBadRequestError


class GithubWebhook:
    def __init__(self, event_type, body_json):
        self.event_type = event_type
        self.body_json = body_json

    @staticmethod
    def from_request(request):
        if 'X-GitHub-Event' not in request.headers:
            raise GithubWebhookBadRequestError('missing X-GitHub-Event header')
        elif request.json is None:
            raise GithubWebhookBadRequestError('request body is not a valid JSON')

        event_type = request.headers['X-GitHub-Event'].lower()

        return GithubWebhook(event_type, request.json)
