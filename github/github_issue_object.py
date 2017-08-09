import re

from github.exceptions import GithubWebhookMalformedEventError
from habitica.habitica_api import HabiticaAPIClient
from habitica.habitica_task import HabiticaTask


class GithubIssueObject:
    def __init__(self, number, title, body, labels):
        self.number = number
        self.title = title
        self.body = body
        self.labels = labels
        self.alias = self.get_task_alias(number)
        self.habitica_task_difficulty = self.get_difficulty(body)

    @staticmethod
    def from_json(js):
        if 'issue' not in js:
            raise GithubWebhookMalformedEventError('issues', 'missing "issue" object')
        elif 'number' not in js['issue']:
            raise GithubWebhookMalformedEventError('issues', 'missing "number" field in issue object')
        elif 'title' not in js['issue']:
            raise GithubWebhookMalformedEventError('issues', 'missing "title" field in issue object')
        elif 'labels' not in js['issue']:
            raise GithubWebhookMalformedEventError('issues', 'missing "labels" field in issue object')

        return GithubIssueObject(
            number = js['issue']['number'],
            title = js['issue']['title'],
            body = js['issue'].get('body', ''),
            labels = map(GithubIssueObject.parse_label, js['issue']['labels']))

    @staticmethod
    def parse_label(json):
        if 'name' not in json:
            raise GithubWebhookMalformedEventError('issues', 'missing "name" field in label object')

        return json['name']

    def label_assigned(self, label):
        return label in self.labels

    @staticmethod
    def get_task_alias(number):
        return f'github_issue_{number}'

    @staticmethod
    def get_difficulty(body):
        difficulties = re.findall(r'difficulty:\s*(\w*)', body.lower())

        if not difficulties:
            return HabiticaTask.EASY_TASK

        difficulty = HabiticaTask.string_to_difficulty(difficulties[-1])

        if difficulty is None:
            return HabiticaTask.EASY_TASK

        return difficulty
