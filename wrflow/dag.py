import logging
from wrflow.model import Edge
from wrflow.model import Node

logger = logging.getLogger(__name__)


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
