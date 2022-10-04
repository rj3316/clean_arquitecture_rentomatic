from .factory import Factory
from ..requests.builder_room_read_request import BuilderRoomReadRequest
from ..requests.builder_hotel_read_request import BuilderHotelReadRequest
from ..requests.builder_converter_read_request import BuilderConverterReadRequest

class FactoryBuilder(Factory):
    @classmethod
    def create(cls, domain = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                ret_val = BuilderRoomReadRequest
            elif domain == 'hotel':
                ret_val = BuilderHotelReadRequest
            elif domain == 'converter':
                ret_val = BuilderConverterReadRequest

        return ret_val