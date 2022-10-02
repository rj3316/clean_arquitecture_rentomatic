import uuid
import json

from ...domain.hotel import Hotel
from ...serializers.hotel import HotelJsonEncoder

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

def test_Hotel_model_init():
    hotel = Hotel(
        code,
        nif = nif,
        name = name,
        rooms = rooms,
    )

    assert hotel.code == code
    assert hotel.nif == nif
    assert hotel.name == name
    assert hotel.rooms == rooms

def test_Hotel_model_from_dict():
    hotel = Hotel.from_dict(init_dict)

    assert hotel.code == code
    assert hotel.nif == nif
    assert hotel.name == name
    assert hotel.rooms == rooms

def test_Hotel_model_to_dict():
    hotel = Hotel.from_dict(init_dict)

    assert hotel.to_dict() == init_dict

def test_Hotel_model_comparison():
    hotel1 = Hotel.from_dict(init_dict)
    hotel2 = Hotel.from_dict(init_dict)

    assert hotel1 == hotel2

def test_Hotel_model_serializer():
    hotel = Hotel.from_dict(init_dict)

    json_expected = f"""
        {{
            "code": "{code}",
            "nif": "{nif}",
            "name": "{name}",
            "rooms": {rooms}
        }}
    """

    json_hotel = json.dumps(hotel, cls = HotelJsonEncoder)

    dict_json_hotel = json.loads(json_hotel)
    dict_json_expected = json.loads(json_expected)

    assert dict_json_hotel == dict_json_expected
