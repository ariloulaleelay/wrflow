
__all__ = [
    'Task',
]


class Task(object):

    @classmethod
    def required_events(cls, produced_events):
        raise NotImplemented("required_events should be implemented")

    @classmethod
    def produced_events(cls, required_events):
        raise NotImplemented("produced_events should be implementead")

    def run(self, required_events):
        raise NotImplemented("run should be implemented")

    def pool(self, required_events):
        return []
