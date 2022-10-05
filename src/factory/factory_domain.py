from ..domain.room import Room
from ..domain.hotel import Hotel
from ..domain.converter import Converter

class FactoryDomain:
    @classmethod
    def create(cls, domain = None, config = None):
        is_list = isinstance(config, list)
        is_dict = isinstance(config, dict)
        is_none = config is None
        is_valid = is_list or is_dict or is_none

        ret_val = None

        if is_valid and (domain is not None):
            if not is_list: config = [config]
            ret_val =  [cls._create(domain, i) for i in config]
            if not is_list: ret_val = ret_val[0]
        return ret_val

    @classmethod
    def _create(cls, domain, config):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                if isinstance(config, dict): ret_val = Room.from_dict(config)
                else: ret_val = Room()
            elif domain == 'hotel':
                if isinstance(config, dict): ret_val = Hotel.from_dict(config)
                else: ret_val = Hotel()
            elif domain == 'converter':
                if isinstance(config, dict): ret_val = Converter.from_dict(config)
                else: ret_val = Converter()

        return ret_val
