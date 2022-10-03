from collections.abc import Mapping

class RoomReadInvalidRequest:
    def __init__(self):
        self.errors = list()
    
    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        return len(self.errors) > 0
    
    def __bool__(self):
        return False
    
class RoomReadValidRequest:
    def __init__(self, filters = None):
        self.filters = filters
    
    def __bool__(self):
        return True


class BuilderRoomReadRequest:
    @classmethod
    def build_room_read_request(cls, filters = None):
        accepted_filters = ['code__eq', 'price__eq', 'price__lt', 'price__gt']
        invalid_req = RoomReadInvalidRequest()

        if filters is not None:
            if not isinstance(filters, Mapping):
                invalid_req.add_error('filters', "Is not iterable")
                return invalid_req
            
            for key, _ in filters.items():
                if key not in accepted_filters:
                    invalid_req.add_error('filters', f"Key {key} cannot be used")
                    return invalid_req
        
        return RoomReadValidRequest(filters = filters)