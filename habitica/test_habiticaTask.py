import json
from json import JSONDecodeError
from unittest import TestCase

from habitica.exceptions import HabiticaClientAPIMalformedObjectError
from habitica.habitica_task import HabiticaTask


class TestHabiticaTask(TestCase):
    def test_deserializing_strings_and_jsons(self):
        task_from_str = HabiticaTask.from_json('{"alias": "alias", "id": "id", "completed": false, "priority": 1.0, "type": "todo"}')
        task_from_json = HabiticaTask.from_json(json.loads('{"alias": "alias", "id": "id", "completed": false, "priority": 1.0, "type": "todo"}'))

        self.assertEqual(task_from_str, task_from_json)

    def test_deserializing(self):
        task = HabiticaTask.from_json('{"alias": "alias", "id": "id", "completed": false, "priority": 1.0, "type": "todo"}')

        self.assertEqual(task.type, 'todo', 'task should be todo')
        self.assertFalse(task.done, 'task should be done')
        self.assertEqual(task.difficulty, 1.0, 'task difficulty should be 1.0')
        self.assertEqual(task.alias, 'alias', 'task alias should be alias')
        self.assertEqual(task.id, 'id', 'task id should be "2b774d70-ec8b-41c1-8967-eb6b13d962ba"')

    def test_deserializing_errors(self):
        self.assertRaises(HabiticaClientAPIMalformedObjectError, HabiticaTask.from_json, '{"id": "id", "completed": false, "priority": 1.0, "type": "todo"}')
        self.assertRaises(HabiticaClientAPIMalformedObjectError, HabiticaTask.from_json, '{"alias": "alias", "completed": false, "priority": 1.0, "type": "todo"}')
        self.assertRaises(HabiticaClientAPIMalformedObjectError, HabiticaTask.from_json, '{"alias": "alias", "id": "id", "priority": 1.0, "type": "todo"}')
        self.assertRaises(HabiticaClientAPIMalformedObjectError, HabiticaTask.from_json, '{"alias": "alias", "id": "id", "completed": false, "type": "todo"}')
        self.assertRaises(HabiticaClientAPIMalformedObjectError, HabiticaTask.from_json, '{"alias": "alias", "id": "id", "completed": false, "priority": 1.0}')
        self.assertRaises(JSONDecodeError, HabiticaTask.from_json, '{')

    def test_get_difficulty(self):
        self.assertEqual(HabiticaTask.string_to_difficulty('trivial'), 0.1, 'difficulty should have been 0.1')
        self.assertEqual(HabiticaTask.string_to_difficulty('easy'), 1, 'difficulty should have been 1')
        self.assertEqual(HabiticaTask.string_to_difficulty(' medium'), 1.5, 'difficulty should have been 1.5')
        self.assertEqual(HabiticaTask.string_to_difficulty('hard '), 2, 'difficulty should have been 2')
