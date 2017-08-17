import logging
import os

import requests

from habitica.exceptions import *
from habitica.habitica_task import HabiticaTask


class HabiticaAPIClient:
    '''
    A Habitica API client that deals with todo tasks.
    '''

    def __init__(self):
        if 'USER_KEY' not in os.environ:
            raise HabiticaCLientConfigError('missing user key configuration')

        if 'API_KEY'not in os.environ:
            raise HabiticaCLientConfigError('missing api key configuration')

        self.auth_headers = {
            'x-api-user': os.environ['USER_KEY'],
            'x-api-key': os.environ['API_KEY']
        }

    def get_todo_task(self, alias):
        '''
        Gets a task by its alias.

        :param alias:  The alias of the task to get.
        :return:       The task instance if it exists, None otherwise.
        '''
        result = self._make_get_api_call(f'https://habitica.com/api/v3/tasks/{alias}', True)

        if 'data' not in result:
            return None

        task = HabiticaTask.from_json(result['data'])

        if task.type != 'todo':
            return None

        return task

    def create_new_todo_task(self, alias, title, difficulty):
        '''
        Create a new todo task.

        :param alias:       The alias to create the task with.
        :param title:       The title to give the new task.
        :param difficulty:  The difficulty of the new task.
        '''
        task = self.get_todo_task(alias)

        if task is not None:
            logging.info(f'task "{alias}" already exists, skipping creation')

            return

        request_body = {
            'text': title,
            'type': 'todo',
            'alias': alias,
            'priority': difficulty
        }

        logging.info(f'creating task "{alias}"')

        self._make_post_api_call('https://habitica.com/api/v3/tasks/user', request_body)

    def complete_todo_task(self, alias, title=None, difficulty=HabiticaTask.EASY_TASK):
        '''
        Sets a todo task as complete, creating it if necessary.

        :param alias:       The alias of the task to complete.
        :param title:       A title to use for creation if a task does not exist, or None to not create it.
        :param difficulty:  The difficulty to create the task with.
        '''
        task = self.get_todo_task(alias)

        if task is None:
            if title is not None:
                logging.info(f'task "{alias}" did not exist, creating a new one')

                self.create_new_todo_task(alias, title, difficulty)
                self.complete_todo_task(alias)

                return
            else:
                logging.info(f'failed finding task "{alias}", not completing')

                return
        elif task.done:
            logging.info(f'task "{alias}" already complete, skipping')

            return

        logging.info(f'completing task "{alias}"')
        request_body = {}
        self._make_post_api_call(f'https://habitica.com/api/v3/tasks/{task.id}/score/up', request_body)

    def uncomplete_todo_task(self, alias, title=None, difficulty=HabiticaTask.EASY_TASK):
        '''
        Sets a todo task as uncomplete, creating it if necessary.

        :param alias:       The alias of the task to uncomplete.
        :param title:       A title to use for creation if a task does not exist, or None to not create it.
        :param difficulty:  The difficulty to create the task with.
        '''
        task = self.get_todo_task(alias)

        if task is None:
            if title is not None:
                logging.info(f'task "{alias}" did not exist, creating a new one')

                self.create_new_todo_task(alias, title, difficulty)

                return
            else:
                logging.info(f'failed finding task "{alias}", not uncompleting')

                return
        elif not task.done:
            logging.info(f'task "{alias}" already uncomplete, skipping')

            return

        logging.info(f'uncompleting task "{alias}"')
        request_body = {}
        self._make_post_api_call(f'https://habitica.com/api/v3/tasks/{task.id}/score/down', request_body)

    def delete_todo_task(self, alias):
        '''
        Delete a todo task, if the task does not exist, nothing will be changed.

        :param alias:  The alias of the task to delete.
        '''
        task = self.get_todo_task(alias)

        if task is None:
            logging.info(f'failed finding task "{alias}", not deleting')

            return

        logging.info('deleting task')
        self._make_delete_api_call(f'https://habitica.com/api/v3/tasks/{alias}')

    def update_todo_task(self, alias, text=None, priority=None):
        '''
        Updates a todo task details.

        :param alias:     The alias of the task to update.
        :param text:      The title to update, or None to not update it.
        :param priority:  The priority to update, or None to not update it.
        '''
        request_body = {}

        if text is not None:
            request_body['text'] = text
        if priority is not None:
            request_body['priority'] = priority

        logging.info('updating task')
        self._make_put_api_call(f'https://habitica.com/api/v3/tasks/{alias}', request_body)

    def _make_post_api_call(self, url, body_dictionary, allow_unknown_resource=False):
        headers = { 'Content-Type': 'application/json' }
        headers.update(self.auth_headers)

        response_json = self._validate_request(lambda: requests.post(url, json=body_dictionary, headers=headers), allow_unknown_resource)

        return response_json

    def _make_get_api_call(self, url, allow_unknown_resource=False):
        response_json = self._validate_request(lambda: requests.get(url, headers=self.auth_headers), allow_unknown_resource)

        return response_json

    def _make_put_api_call(self, url, body_dictionary):
        response_json = self._validate_request(lambda: requests.put(url, json=body_dictionary, headers=self.auth_headers), True)

        return response_json

    def _make_delete_api_call(self, url):
        response_json = self._validate_request(lambda: requests.delete(url, headers=self.auth_headers), True)

        return response_json

    def _validate_request(self, request_lambda, missing_resource_allowed):
        try:
            response = request_lambda()
            status_code = response.status_code
            response_json = response.json()
        except requests.exceptions.Timeout:
            raise HabiticaClientTimeoutError()
        except (requests.exceptions.RequestException, ConnectionError) as e:
            raise HabiticaCLientConnectivityError(f'unknown error: {str(e)}')
        except ValueError:
            raise HabiticaClientIllegalResponseError()
        else:
            self._validate_status_code(status_code, response_json, missing_resource_allowed)

            return response_json

    def _validate_status_code(self, status_code, response_json, missing_resource_allowed):
        if str(status_code)[0] == '2' and 'success' in response_json and response_json['success']:
            return
        elif missing_resource_allowed and status_code == 404 and 'error' in response_json and response_json['error'] == 'NotFound':
            return
        else:
            raise HabiticaClientHttpStatusCodeError(status_code, response_json)
