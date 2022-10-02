import json

class HotelJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            to_serialize = {
                "code": str(obj.code),
                "nif": obj.nif,
                "name": obj.name,
                "rooms": obj.rooms,
            }
            return to_serialize
        except AttributeError:
            return super().default(obj)