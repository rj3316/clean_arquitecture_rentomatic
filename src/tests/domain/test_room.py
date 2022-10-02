import uuid
import json

from ...domain.room import Room
from ...domain.domainfactory import DomainFactory
from ...serializers.factoryserializer import SerializerFactory

domain = 'room'

code = uuid.uuid4()
size = 200
price = 10
longitude = -0.09998975
latitude = 51.75436293

init_dict = {
    'code': code,
    'size': size,
    'price': price,
    'longitude': longitude,
    'latitude': latitude,
}

def test_room_model_init():
    dom = Room(
        code,
        size = size,
        price = price,
        longitude = longitude,
        latitude = latitude,
    )

    assert dom.code == code
    assert dom.size == size
    assert dom.price == price
    assert dom.longitude == longitude
    assert dom.latitude == latitude

def test_room_model_from_dict():
    dom = DomainFactory.create(domain, init_dict)

    assert dom.code == code
    assert dom.size == size
    assert dom.price == price
    assert dom.longitude == longitude
    assert dom.latitude == latitude

def test_room_model_to_dict():
    dom = DomainFactory.create(domain, init_dict)

    assert dom.to_dict() == init_dict

def test_room_model_comparison():
    dom1 = DomainFactory.create(domain, init_dict)
    dom2 = DomainFactory.create(domain, init_dict)

    assert dom1 == dom2

def test_room_model_serializer():
    dom = DomainFactory.create(domain, init_dict)
    serializer = SerializerFactory.create(domain)

    json_expected = f"""
        {{
            "code": "{code}",
            "size": {size},
            "price": {price},
            "longitude": {longitude},
            "latitude": {latitude}
        }}
    """

    json_dom = json.dumps(dom, cls = serializer)

    dict_json_dom = json.loads(json_dom)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_dom == dict_json_expected