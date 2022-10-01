import uuid
import json

from ...domain.room import Room
from ...serializers.room import RoomJsonEncoder

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
    room = Room(
        code,
        size = size,
        price = price,
        longitude = longitude,
        latitude = latitude,
    )

    assert room.code == code
    assert room.size == size
    assert room.price == price
    assert room.longitude == longitude
    assert room.latitude == latitude

def test_room_model_from_dict():
    room = Room.from_dict(init_dict)

    assert room.code == code
    assert room.size == size
    assert room.price == price
    assert room.longitude == longitude
    assert room.latitude == latitude

def test_room_model_to_dict():
    room = Room.from_dict(init_dict)

    assert room.to_dict() == init_dict

def test_room_model_comparison():
    room1 = Room.from_dict(init_dict)
    room2 = Room.from_dict(init_dict)

    assert room1 == room2

def test_room_model_serializer():
    room = Room.from_dict(init_dict)

    json_expected = f"""
        {{
            "code": "{code}",
            "size": {size},
            "price": {price},
            "longitude": {longitude},
            "latitude": {latitude}
        }}
    """

    json_room = json.dumps(room, cls = RoomJsonEncoder)

    assert json.loads(json_room) == json.loads(json_expected)
