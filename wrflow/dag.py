import logging
from wrflow.common import hash_dict
from wrflow.common import hash_list
from copy import copy

logger = logging.getLogger(__name__)


class Node(object):

    def __init__(self, params, demand=0, satisfied=False):
        self.id = hash_dict(params)
        self.params = params
        self.demand = demand
        self.edges = {}
        self.satisfied = satisfied

    def __eq__(self, that):
        return self.id == that.id


class Edge(object):

    def __init__(self, task_class):
        self.task_class = task_class
        self.nodes = {}

    def __eq__(self, that):
        return self.id == that.id

    @property
    def id(self):
        return self.task_class.__name__ + ':' + hash_list(sorted(self.nodes.keys()))

    @property
    def satisfied(self):
        for node in self.nodes.values():
            if not node.satisfied:
                return False
        return True


class DagException(Exception):
    pass


class Dag(object):

    def __init__(self, depth_threshold=1000):
        self._nodes = {}
        self._edges = {}
        self._events = {}
        self._generators = []
        self._depth_threshold = depth_threshold

    def _is_node_terminal(self, node):
        """Return if node parameters already happened in event system
        """

        if node.id in self._events:
            return True

        for event in self._events.itervalues():
            if event.is_applicable(node.params):
                return True
        return False

    def _add_node(self, node, depth=0):
        if depth > self._depth_threshold:
            raise DagException("Node dependency too deep")

        if node.id in self._nodes:
            return self._nodes[id]
        else:
            self._nodes[id] = node

        if self._is_node_terminal(node):
            node.satisfied = True
            return node

        # find node ancestors and generators
        for generator_class in self._generators:
            required_events = generator_class.required_events(node.params)
            if required_events is None:
                continue
            for events_join in required_events:
                edge = Edge(generator_class)
                for event in events_join:
                    parent_node = self._add_node(Node(event), depth + 1)
                    edge.nodes[parent_node.id] = parent_node
                if edge.id in self._edges:
                    edge = self._edges[edge.id]
                else:
                    self._edges[edge.id] = edge
                node.edges[edge.id] = edge
        return node

    def add_node(self, node, demand=1):
        node = self._add_node(node)
        nodes_to_process = {node.id: node}
        nodes_seen = set()
        while len(nodes_to_process) > 0:
            id, node = nodes_to_process.popitem()
            nodes_seen.add(id)
            node.demand += demand
            for edge in node.edges.itervalues():
                for node_id, parent_node in edge.nodes.iteritems():
                    if node_id in nodes_seen:
                        continue
                    nodes_to_process[node_id] = parent_node
        return

    def remove_node(self, node):
        pass
