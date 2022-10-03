from collections.abc import Mapping

class ReadInvalidRequest:
    def __init__(self):
        self.errors = list()
    
    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        return len(self.errors) > 0
    
    def __bool__(self):
        return False
    
class ReadValidRequest:
    def __init__(self, filters = None):
        self.filters = filters
    
    def __bool__(self):
        return True


class BuilderReadRequest:
    @classmethod
    def build_read_request(cls, filters = None):
        accepted_filters = ['code__eq', 'price__eq', 'price__lt', 'price__gt']
        invalid_req = ReadInvalidRequest()

        if filters is not None:
            if not isinstance(filters, Mapping):
                invalid_req.add_error('filters', "Is not iterable")
                return invalid_req
            
            for key, _ in filters.items():
                if key not in accepted_filters:
                    invalid_req.add_error('filters', f"Key {key} cannot be used")
                    return invalid_req
        
        return ReadValidRequest(filters = filters)