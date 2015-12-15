from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy import orm
from json import loads as json_loads
from json import dumps as json_dumps
# from datetime import datetime

from wrflow.common import hash_dict

Base = declarative_base()

__all__ = [
    'Event',
]


class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    params_string = Column(String, nullable=False)
    demand = Column(Integer, nullable=False)
    last_occurence = Column(DateTime, nullable=True)

    def __init__(self, params, demand=0):
        self.id = hash_dict(params).hexdigest()
        self.params = params
        self.params_string = json_dumps(self.params)
        self.demand = demand
        self.last_occurence = None

    @orm.reconstructor
    def __init_reconstruct(self):
        self.params = json_loads(self.params_string)

    def is_applicable(self, params):
        for k, v in params.iteritems():
            if self.parsed_params.get(k, None) != v:
                return False
        return True

    def occured(self):
        return self.last_occurence is not None
