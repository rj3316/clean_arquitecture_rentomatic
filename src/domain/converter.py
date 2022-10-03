from .entity import Entity, dataclass

@dataclass
class Converter(Entity):
    serial: str = ''
    host: str = ''
    rated: int = 0
    power: float = 0.0
    soc: float = 0.0
    
