import json

from habitica.exceptions import HabiticaClientAPIMalformedObjectError


class HabiticaTask:
    TRIVIAL_TASK = 0.1
    EASY_TASK = 1
    MEDIUM_TASK = 1.5
    HARD_TASK = 2

    def __init__(self, alias, task_id, done, difficulty, task_type):
        self.alias = alias
        self.id = task_id
        self.done = done
        self.difficulty = difficulty
        self.type = task_type

    @staticmethod
    def from_json(js):
        if type(js) is str:
            js = json.loads(js)

        if 'alias' not in js:
            raise HabiticaClientAPIMalformedObjectError('task', 'missing "alias" field')
        elif 'id' not in js:
            raise HabiticaClientAPIMalformedObjectError('task', 'missing "id" field')
        elif 'completed' not in js:
            raise HabiticaClientAPIMalformedObjectError('task', 'missing "completed" field')
        elif 'priority' not in js:
            raise HabiticaClientAPIMalformedObjectError('task', 'missing "priority" field')
        elif 'type' not in js:
            raise HabiticaClientAPIMalformedObjectError('task', 'missing "type" field')

        return HabiticaTask(js['alias'], js['id'], js['completed'], js['priority'], js['type'])

    @staticmethod
    def string_to_difficulty(s):
        s = s.strip().lower()

        if s == 'trivial':
            return HabiticaTask.TRIVIAL_TASK
        if s == 'easy':
            return HabiticaTask.EASY_TASK
        if s == 'medium':
            return HabiticaTask.MEDIUM_TASK
        if s == 'hard':
            return HabiticaTask.HARD_TASK

        return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)

        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
