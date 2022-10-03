from .entity import Entity, dataclass

@dataclass
class Hotel(Entity):
    nif: str = ''
    name: str = ''
    rooms: int = 0
