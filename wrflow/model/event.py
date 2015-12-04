from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy import orm
from json import loads as json_loads
from json import dumps as json_dumps
from datetime import datetime

from wrflow.common import hash_dict

Base = declarative_base()

__all__ = [
    'Event',
]


class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    params = Column(String, nullable=False)
    last_occurence = Column(DateTime, nullable=False)

    def __init__(self, parsed_params):
        self.id = hash_dict(parsed_params).hexdigest()
        self.params = json_dumps(parsed_params)
        self.parsed_params = parsed_params
        self.last_occurence = datetime.now()

    @orm.reconstructor
    def __init_reconstruct(self):
        self.parsed_params = json_loads(self.params)

    def is_applicable(self, params):
        for k, v in params.iteritems():
            if self.parsed_params.get(k, None) != v:
                return False
        return True
