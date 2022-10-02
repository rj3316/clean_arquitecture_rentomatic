import uuid
import json

from ...domain.hotel import Hotel
from ...domain.domainfactory import DomainFactory
from ...serializers.factoryserializer import SerializerFactory

domain = 'hotel'

code = uuid.uuid4()
nif = 'B12345678'
name = 'Hoteles Paco'
rooms = 10

init_dict = {
    'code': code,
    'nif': nif,
    'name': name,
    'rooms': rooms,
}

def test_hotel_model_init():
    dom = Hotel(
        code,
        nif = nif,
        name = name,
        rooms = rooms,
    )

    assert dom.code == code
    assert dom.nif == nif
    assert dom.name == name
    assert dom.rooms == rooms

def test_hotel_model_from_dict():
    dom = DomainFactory.create(domain, init_dict)[0]

    assert dom.code == code
    assert dom.nif == nif
    assert dom.name == name
    assert dom.rooms == rooms

def test_hotel_model_to_dict():
    dom = DomainFactory.create(domain, init_dict)[0]

    assert dom.to_dict() == init_dict

def test_hotel_model_comparison():
    hotel1 = DomainFactory.create(domain, init_dict)[0]
    hotel2 = DomainFactory.create(domain, init_dict)[0]  

    assert hotel1 == hotel2

def test_hotel_model_serializer():
    dom = DomainFactory.create(domain, init_dict)[0]

    serializer = SerializerFactory.create(domain)

    json_expected = f"""
        {{
            "code": "{code}",
            "nif": "{nif}",
            "name": "{name}",
            "rooms": {rooms}
        }}
    """

    json_dom = json.dumps(dom, cls = serializer)

    dict_json_dom = json.loads(json_dom)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_dom == dict_json_expected
