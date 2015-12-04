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
    params = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(Integer, nullable=False, default=0)

    def __init__(self, classname, params, status='queue', priority=0):
        self.classname = classname
        self.params = json_dumps(params)
        self.parsed_params = params
        self.status = status
        self.priority = priority
        hash = sha1()
        hash.update(classname)
        hash.update('\0')
        for k in sorted(params.keys):
            hash.update(k)
            hash.update('\0')
            hash.update(params[k])
            hash.update('\0')

    @orm.reconsructor
    def __init_reconstruct(self):
        self.parsed_params = json_loads(self.params)

    @property
    def parsed_params(self):
        if self.__parsed_params is None:
            self.__parsed_params = json_loads(self.params)
        return self.__parsed_params
