from .room import Room
from .hotel import Hotel

class DomainFactory:
    @classmethod
    def create_domain(cls, domain = None, config = None):
        ret_val = None

        if domain is not None:
            if domain == 'room':
                if isinstance(config, dict): ret_val = Room.from_dict(config)
                else: ret_val = Room()
            elif domain == 'hotel':
                if isinstance(config, dict): ret_val = Hotel.from_dict(config)
                else: ret_val = Hotel()

        return ret_val

    @classmethod
    def from_dicts(cls, domain, dicts):
        return [cls.create_domain(domain, i) for i in dicts]