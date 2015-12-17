from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy import orm
from json import loads as json_loads
from json import dumps as json_dumps

from wrflow.common import hash_dict, hash_list

Base = declarative_base()

__all__ = [
    'Node',
    'Edge',
]


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True)
    params_string = Column(String, nullable=False)
    demand = Column(Integer, nullable=False)
    satisfied = Column(Boolean, nullable=False)
    edges = orm.relationship("Edge")
    last_occurence = Column(DateTime, nullable=True)

    def __init__(self, params, demand=0, satisfied=False):
        self.id = hash_dict(params)
        self.params = params
        self.params_string = json_dumps(self.params)
        self.demand = demand
        self.satisfied = satisfied
        self.last_occurence = None

    @classmethod
    def get_or_create(cls, params, session=None):
        if session is None:
            session = cls
        id = hash_dict(params)
        instance = session.query(cls).filter(cls.id == id).first()
        if instance:
            return instance, False
        instance = Node(params)
        session.add(instance)
        return instance, True

    @orm.reconstructor
    def __init_reconstruct(self):
        self.params = json_loads(self.params_string)

    def is_sub_of(self, node):
        for k, v in node.params.iteritems():
            if self.params.get(k, None) != v:
                return False
        return True

    def occured(self):
        return self.last_occurence is not None

    def satisfy(self, session):
        self.satisfied = True
        nodes = session.query(Node).filter(~Node.satisfied)
        for node in nodes:
            if self.is_sub_of(node):
                node.satisfied = True

    def add_demand(self, demand, session):
        seen_nodes = set()
        nodes = set()
        nodes.add(self)
        while len(nodes) > 0:
            node = nodes.pop()
            node.demand += demand
            seen_nodes.add(node)
            for edge in node.edges:
                for subnode in edge.nodes:
                    if subnode in seen_nodes:
                        continue
                    if subnode.satisfied:
                        continue
                    nodes.add(subnode)
        for node in seen_nodes:
            node.save()

    def __eq__(self, that):
        return self.id == that.id

    def __hash__(self):
        return hash(self.id)


class Edge(Base):
    __tablename__ = 'edges'

    id = Column(String, primary_key=True)
    task_class_string = Column(String, nullable=False)
    nodes = orm.relationship("Node")

    def __init__(self, task_class, nodes):
        self.task_class = task_class
        self.task_class_string = self.task_class.__module__ + '.' + self.task_class.__name__
        self.id = self._generate_id(task_class, nodes)
        for node in nodes:
            self.nodes.append(node)

    @orm.reconstructor
    def __init_reconstruct(self):
        module_name, class_name = self.task_class_string.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        self.task_class = getattr(module, class_name)

    @classmethod
    def _generate_id(cls, task_class, nodes):
        task_class_string = task_class.__module__ + '.' + task_class.__name__
        id = task_class_string + ':' + hash_list(sorted(map(lambda x: x.id, nodes)))
        return id

    def __eq__(self, that):
        return self.id == that.id

    @classmethod
    def get_or_create(cls, task_class, nodes, session):
        id = cls._generate_id(task_class, nodes)
        instance = session.query(cls).filter(cls.id == id).first()
        if instance:
            return instance, False
        instance = cls(task_class, nodes)
        session.add(instance)
        return instance, True

    @property
    def satisfied(self):
        for node in self.nodes:
            if not node.satisfied:
                return False
        return True
