import json

class ConverterJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            to_serialize = {
                "code": str(obj.code),
                "serial": obj.serial,
                "host": obj.host,
                "rated": obj.rated,
                "power": obj.power,
                "soc": obj.soc,
            }
            return to_serialize
        except AttributeError:
            return super().default(obj)