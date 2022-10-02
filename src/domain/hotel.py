from dataclasses import dataclass

from .entity import Entity

@dataclass
class Hotel(Entity):
    nif: str = ''
    name: str = ''
    rooms: int = 0
