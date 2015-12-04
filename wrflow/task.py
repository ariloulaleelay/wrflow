
__all__ = [
    'Task',
]


class Task(object):

    @classmethod
    def required_events(cls, params):
        raise NotImplemented("required_events should be implemented")

    @classmethod
    def produced_events(cls, params):
        raise NotImplemented("produced_events should be implementead")

    def run(self, params):
        raise NotImplemented("run should be implemented")

    def pool(self, params):
        return []
