from .room import RoomJsonEncoder
from .hotel import HotelJsonEncoder

class SerializerFactory:
    @classmethod
    def create(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = RoomJsonEncoder
            elif domain == 'hotel':
                ret_val = HotelJsonEncoder

        return ret_val