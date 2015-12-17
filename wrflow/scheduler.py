import logging

# from wrflow.model import TaskInstance
from wrflow.model import Node
from wrflow.model import Edge
from wrflow import Task
from sqlalchemy.orm.session import sessionmaker

logger = logging.getLogger(__name__)

__all__ = [
    'Scheduler',
]

Session = sessionmaker()


class Scheduler(object):

    def __init__(self, config):
        self._task_classes = {}
        self._config = config
        self.depth_threshold = 1000
        for class_name in config.task_generators:
            self._get_task_by_class_name(class_name)

    def _open_session(self):
        return Session()

    def _get_task_by_class_name(self, class_name):
        if class_name not in self._known_task_classes:
            module_name, class_name = class_name.rsplit('.', 1)
            module = __import__(module_name)
            class_instance = getattr(module, class_name)
            if not issubclass(class_instance, Task):
                raise TypeError("%s should be subclass of wrflow.Task" % class_name)
            self._task_classes[class_name] = class_instance
        return self._task_classes[class_name]

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

    def add_node(self, params, demand, depth=0, session=None):
        session_was_none = session is None
        if session_was_none:
            session = self._open_session()
        node, created = Node.get_or_create(params, session)
        if not created:
            return node
        if depth < self.depth_threshold:
            self._extend_graph(node, depth, session)
        if demand > 0:
            node.add_demand(demand)
        if session_was_none:
            session.commit()
        return node

    def add_event(self, params):
        session = self._open_session()
        node, _ = Node.get_or_create(params, session)
        node.satisfy(session)
        session.commit()

    def _extend_graph(self, node, depth, session):
        for task_class in self._task_classes.iteritems():
            required_events = task_class.required_events(node.params)
            if required_events is None:
                continue
            for events_pack in required_events:
                # at this point we will generate edge
                subnodes = []
                for single_event_params in events_pack:
                    subnode = self.add_node(single_event_params, 0, depth=depth+1, session=session)
                    subnodes.append(subnode)
                edge, created = Edge.get_or_create(task_class, subnodes, session)
                node.edges.append(edge)
