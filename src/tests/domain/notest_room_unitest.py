import unittest
import uuid
import json

from ...domain.room import Room
from ...serializers.room import RoomJsonEncoder

class TestRoom(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.code = uuid.uuid4()
        cls.size = 200
        cls.price = 10
        cls.longitude = -0.09998975
        cls.latitude = 51.75436293

        cls.init_dict = {
            'code': cls.code,
            'size': cls.size,
            'price': cls.price,
            'longitude': cls.longitude,
            'latitude': cls.latitude,
        }

    def test_room_model_init(self):
        room = Room(
            self.code,
            size = self.size,
            price = self.price,
            longitude = self.longitude,
            latitude = self.latitude,
        )

        assert room.code == self.code
        assert room.size == self.size
        assert room.price == self.price
        assert room.longitude == self.longitude
        assert room.latitude == self.latitude

    def test_room_model_from_dict(self):
        room = Room.from_dict(self.init_dict)

        assert room.code == self.code
        assert room.size == self.size
        assert room.price == self.price
        assert room.longitude == self.longitude
        assert room.latitude == self.latitude

    def test_room_model_to_dict(self):
        room = Room.from_dict(self.init_dict)

        assert room.to_dict() == self.init_dict

    def test_room_model_comparison(self):
        room1 = Room.from_dict(self.init_dict)
        room2 = Room.from_dict(self.init_dict)

        assert room1 == room2

    def test_room_model_serializer(self):
        room = Room.from_dict(self.init_dict)

        json_expected = f"""
            {{
                "code": "{self.code}",
                "size": {self.size},
                "price": {self.price},
                "longitude": {self.longitude},
                "latitude": {self.latitude}
            }}
        """

        json_room = json.dumps(room, cls = RoomJsonEncoder)

        j_room = json.loads(json_room)
        j_expected = json.loads(json_expected)

        assert j_room == j_expected

if __name__ == '__main__':
    unittest.main(verbosity = 2)