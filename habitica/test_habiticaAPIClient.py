from unittest import TestCase

from httmock import HTTMock, all_requests, response

from habitica.habitica_api import HabiticaAPIClient


class TestHabiticaAPIClient(TestCase):
    def test_get_existing_todo_task(self):
        get_task_url_path = '/api/v3/tasks/alias'

        @all_requests
        def requests_mock(url, request):
            if url.path == get_task_url_path:
                return '{"success":true,"data":{"_id":"2b774d70-ec8b-41c1-8967-eb6b13d962ba","text":"test task","alias":"alias","type":"todo","priority":1.5,"completed":false,"id":"2b774d70-ec8b-41c1-8967-eb6b13d962ba"}}'

            return '{ "success": false, "NotFound": "The specified task could not be found." }'

        with HTTMock(requests_mock):
            task = HabiticaAPIClient().get_todo_task('alias')
            self.assertEqual(task.type, 'todo', 'task should be todo')
            self.assertFalse(task.done, 'task should be done')
            self.assertEqual(task.difficulty, 1.5, 'task difficulty should be 1.5')
            self.assertEqual(task.alias, 'alias', 'task alias should be alias')
            self.assertEqual(task.id, '2b774d70-ec8b-41c1-8967-eb6b13d962ba', 'task id should be "2b774d70-ec8b-41c1-8967-eb6b13d962ba"')

    def test_get_existing_todo_task(self):
        @all_requests
        def requests_mock(url, request):
            return response(404, '{ "success": false, "error": "NotFound" }')

        with HTTMock(requests_mock):
            self.assertIsNone(HabiticaAPIClient().get_todo_task('alias'), 'returned task should be None')

    def test_get_existing_todo_task(self):
        @all_requests
        def requests_mock(url, request):
            return response(404, '{ "success": false, "error": "NotFound" }')

        with HTTMock(requests_mock):
            self.assertIsNone(HabiticaAPIClient().get_todo_task('alias'), 'returned task should be None')
