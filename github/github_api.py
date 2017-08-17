import logging

from github.exceptions import GithubWebhookMalformedEventError
from github.github_issue_object import GithubIssueObject
from github.github_webhook import GithubWebhook


class GithubWebhookHandler:
    def __init__(self, habitica_api_client, ignored_label=None):
        self.habitica_api_client = habitica_api_client
        self.ignored_label = ignored_label

    def handle_webhook(self, request):
        webhook = GithubWebhook.from_request(request)

        if webhook.event_type == 'issues':
            self.handle_issues_event(webhook.body_json)
        else:
            logging.info(f'unknown event "{webhook.event_type}", skipping')

    def handle_issues_event(self, request_json):
        if 'action' not in request_json:
            raise GithubWebhookMalformedEventError('issues', 'missing "action" field')

        logging.info(f'handling issues event')

        action = request_json['action'].lower()
        issue = GithubIssueObject.from_json(request_json)

        if issue.label_assigned(self.ignored_label) and issue == 'labeled':
            logging.info('ignore label is set, task will be deleted if required')

            self.delete_task_if_exists(issue)
        elif action == 'opened':
            self.handle_issue_opened(issue)
        elif action == 'reopened':
            self.handle_issue_reopenened(issue)
        elif action == 'closed':
            self.handle_issue_closed(issue)
        elif action == 'edited':
            self.handle_issue_edited(issue)
        else:
            logging.info(f'ignoring unhandled issues action {action}')

    def delete_task_if_exists(self, issue):
        task = self.habitica_api_client.get_todo_task(issue.alias)

        if task is not None:
            self.habitica_api_client.delete_todo_task(issue.alias)

    def handle_issue_opened(self, issue):
        logging.info(f'issue {issue.number} titled "{issue.title}" opened')

        self.habitica_api_client.create_new_todo_task(issue.alias, issue.title, issue.habitica_task_difficulty)

    def handle_issue_reopenened(self, issue):
        logging.info(f'issue {issue.number} titled "{issue.title}" reopened')

        self.habitica_api_client.uncomplete_todo_task(issue.alias, issue.title, issue.habitica_task_difficulty)

    def handle_issue_closed(self, issue):
        logging.info(f'issue {issue.number} titled "{issue.title}" closed')

        self.habitica_api_client.complete_todo_task(issue.alias, issue.title, issue.habitica_task_difficulty)

    def handle_issue_edited(self, issue):
        logging.info(f'issue {issue.number} titled "{issue.title}" edited')

        self.habitica_api_client.update_todo_task(issue.alias, issue.title, issue.habitica_task_difficulty)
