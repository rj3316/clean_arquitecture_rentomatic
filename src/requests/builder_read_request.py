from collections.abc import Mapping

from .requests import ReadValidRequest, ReadInvalidRequest

class BuilderReadRequest:
    @classmethod
    def build_read_request(cls, filters = None):
        accepted_filters = cls._get_accepted_filters(None)

        invalid_req = ReadInvalidRequest()

        if filters is not None:
            if not isinstance(filters, Mapping):
                invalid_req.add_error('filters', "Is not iterable")
                return invalid_req
            
            for key, _ in filters.items():
                if key not in accepted_filters:
                    invalid_req.add_error('filters', f"Key {key} cannot be used as filter <field>__<logic>")
                    return invalid_req
        
        return ReadValidRequest(filters = filters)

    def _get_accepted_filters(self):
        return list()