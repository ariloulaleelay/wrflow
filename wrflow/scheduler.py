import logging

# from wrflow.common import hash_dict
# from wrflow.model import TaskInstance
from wrflow.model import Event
from wrflow import Task

logger = logging.getLogger(__name__)

__all__ = [
    'Scheduler',
]


class Scheduler(object):

    def __init__(self):
        self._known_task_classes = {}
        self._events = {}
        self._tasks = {}
        self._tasks_ready_to_run = {}
        self._tasks_running = {}
        self._tasks_waiting = {}

    def _get_task_by_class_name(self, classname):
        if classname not in self._known_task_classes:
            module_name, class_name = classname.rsplit('.', 1)
            module = __import__(module_name)
            class_instance = getattr(module, class_name)
            if not issubclass(class_instance, Task):
                raise TypeError("%s should be subclass of wrflow.Task" % classname)
            self._known_tasks[classname] = class_instance
        return self._known_task_classes[classname]

    def find_events(self, params):
        """Find events by params mask
        """
        result = []
        for event in self._events.itervalues():
            if event.is_applicable(params):
                result.append(event)
        return result

    def is_params_happened(self, params):
        for event in self._events.itervalues():
            if event.is_applicable(params):
                return True
        return False

    def require_event(self, params, demand=1):
        event = Event(params, demand)

        if event.id in self._events:
            event = self._events[event.id]
            if demand > event.demand:
                event.demand = demand
                event.save()
            return

        self._events[event.id] = event
        event.save()

    def _get_event_ancestors(self, event, seen_events=None):
        found = False
        for class_name, class_obj in self._known_task_classes.iteritems():
            required_events = class_obj.required_events(event.params)
            if required_events is None:
                continue
            for event_conjunction in required_events:
                for single_event_params in event_conjunction:
                    if self.is_params_happened:
                        continue
                    found = found or self.require_event(single_event_params, demand, seen_events)
        return found

    def generate_current_dag(self):
        pass

    def schedule_tasks_by_required_events(self):
        pass
