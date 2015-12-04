import logging

from wrflow.common import hash_dict

logger = logging.getLogger(__name__)

__all__ = [
    'Scheduler',
]


class TaskQueueEntry(object):

    def __init__(self, task_class, task_params, priority, required_events, produced_events):
        self.task_class = task_class
        self.task_params = task_params
        self.priority = priority
        self.required_events = required_events
        self.produced_events = produced_events
        self.id = task_class.__name__ + '-' + hash_dict(task_params)


class Scheduler(object):

    def __init__(self):
        self._known_task_classes = {}
        self._events = {}
        self._required_events = {}
        self._required_events_queue = []
        self._tasks_ready_to_run = {}
        self._tasks_running = {}
        self._tasks_waiting_for_events = {}

    def _get_task_by_class_name(self, classname):
        if classname not in self._known_task_classes:
            module_name, class_name = classname.rsplit('.', 1)
            module = __import__(module_name)
            class_instance = getattr(module, class_name)
            if not issubclass(class_instance, Task):
                raise TypeError("%s should be subclass of wrflow.Task" % classname)
            self._known_tasks[classname] = class_instance
        return self._known_task_classes[classname]

    def add_task(self, classname, params, priority=1):
        task_class = self._get_task_by_class_name(classname)
        self._add_task_queue.append([task_class, params, priority])
        required_events = task_class.required_events(params)
        if required_events is None:
            raise TypeError("task could not be scheduled with such params")
        produced_events = task_class.produced_events(params)
        queue_entry = TaskQueueEntry(task_class, params, priority, required_events, produced_events)
        if new_task_only and queue_entry.id in self._tasks_waiting_for_events:
            return
        self._tasks_waiting_for_events[queue_entry.id] = queue_entry

    def update_ready_to_run(self):
        for task_key, task in self._tasks_waiting_for_events.iteritems():
            required_events =

    def schedule_tasks_by_required_events(self):

