from .room import Room
from .hotel import Hotel
from .converter import Converter

class DomainFactory:
    @classmethod
    def create(cls, domain = None, config = None):
        ret_val = None

        if domain is not None:
            is_dict = False
            if isinstance(config, dict): is_dict = True

            if not isinstance(config, list): config = [config]

            ret_val =  [cls._create(domain, i) for i in config]
            if is_dict: ret_val = ret_val[0]
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
