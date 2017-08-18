import re

from github.exceptions import GithubWebhookMalformedEventError
from habitica.habitica_task import HabiticaTask


class GithubIssueObject:
    def __init__(self, number, repo_id, title, body, labels):
        self.github_repo_id = repo_id
        self.number = number
        self.title = title
        self.body = body
        self.labels = labels
        self.alias = self.get_task_alias(number, repo_id)
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
        elif 'repository' not in js:
            raise GithubWebhookMalformedEventError('issues', 'missing "repository" object')
        elif 'id' not in js['repository']:
            raise GithubWebhookMalformedEventError('issues', 'missing "repository" object')

        return GithubIssueObject(
            number = js['issue']['number'],
            repo_id= js['repository']['id'],
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
    def get_task_alias(number, github_repo_id):
        return f'repo_{github_repo_id}_issue_{number}'

    @staticmethod
    def get_difficulty(body):
        difficulties = re.findall(r'difficulty:\s*(\w*)', body.lower())

        if not difficulties:
            return HabiticaTask.EASY_TASK

        difficulty = HabiticaTask.string_to_difficulty(difficulties[-1])

        if difficulty is None:
            return HabiticaTask.EASY_TASK

        return difficulty
