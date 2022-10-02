from dataclasses import dataclass

from .entity import Entity

@dataclass
class Room(Entity):
    size: int = 0
    price: int = 0
    longitude: float = 0.0
    latitude: float = 0.0
