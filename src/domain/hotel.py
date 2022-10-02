import dataclasses

from .entity import Entity

@dataclasses.dataclass
class Hotel(Entity):
    nif: str = ''
    name: str = ''
    rooms: int = 0