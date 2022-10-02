import uuid
from dataclasses import dataclass, asdict
from inspect import getmembers

@dataclass
class Entity:
    code: uuid.UUID = ''

    @classmethod
    def from_dict(cls, d = None):
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    def describe(self):
        atts = getmembers(self)

        attributes = list()
        for att in atts:
            c0 = not att[0].startswith('__')
            c1 = not callable(att[1])

            if c0 and c1:
                attribute = (att[0], type(att[1]).__name__)
                attributes.append(attribute)

        return attributes
