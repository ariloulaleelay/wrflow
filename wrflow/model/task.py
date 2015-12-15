from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import orm
from json import loads as json_loads
from json import loads as json_dumps
from hashlib import sha1

Base = declarative_base()

__all__ = [
    'TaskInstance',
]


class TaskInstance(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True)
    classname = Column(String, nullable=False)
    status = Column(String, nullable=False)
    params_string = Column(String, nullable=False)
    required_events_string = Column(String, nullable=False)
    produced_events_string = Column(String, nullable=False)
    priority = Column(Integer, nullable=False, default=0)

    def __init__(self, classname, params, required_events, produced_events, status='queue', priority=0):
        self.classname = classname
        self.status = status
        self.priority = priority
        self.params = params
        self.required_events = required_events
        self.produced_events = produced_events

        hash = sha1()
        hash.update(classname)
        hash.update('\0')
        for k in sorted(params.keys):
            hash.update(k)
            hash.update('\0')
            hash.update(params[k])
            hash.update('\0')
        self.id = hash.hexdigest()

        self.__init_construct()

    @orm.reconsructor
    def __init_reconstruct(self):
        self.params = json_loads(self.params_string)
        self.required_events = json_loads(self.required_events_string)
        self.produced_events = json_loads(self.produced_events_string)

    def __init_construct(self):
        self.params_string = json_dumps(self.params)
        self.required_events_string = json_dumps(self.required_events)
        self.produced_events_string = json_dumps(self.produced_events)
