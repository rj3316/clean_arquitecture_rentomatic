from ..serializers.room import RoomJsonEncoder
from ..serializers.hotel import HotelJsonEncoder
from ..serializers.converter import ConverterJsonEncoder

class FactorySerializer:
    @classmethod
    def create(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = RoomJsonEncoder
            elif domain == 'hotel':
                ret_val = HotelJsonEncoder
            elif domain == 'converter':
                ret_val = ConverterJsonEncoder

        return ret_val