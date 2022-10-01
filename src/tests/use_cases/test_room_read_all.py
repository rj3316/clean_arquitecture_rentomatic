import pytest
import uuid
from unittest import mock

from ...domain.room import Room
from ...use_cases.read_all import room_read_all

size_1 = 215
price_1 = 39
longitude_1 = -0.09998975
latitude_1 = 51.75436293

size_2 = 405
price_2 = 66
longitude_2 = 0.18228006
latitude_2 = 51.74640997

size_3 = 56
price_3 = 60
longitude_3 = 0.27891577
latitude_3 = 51.45994069

size_4 = 93
price_4 = 48
longitude_4 = 0.33894476
latitude_4 = 51.39916678

@pytest.fixture
def domain_rooms():
    room_1 = Room(
        code = uuid.uuid4(),
        size = size_1,
        price = price_1,
        longitude = longitude_1,
        latitude = latitude_1,
    )

    room_2 = Room(
        code = uuid.uuid4(),
        size = size_2,
        price = price_2,
        longitude = longitude_2,
        latitude = latitude_2,
    )

    room_3 = Room(
        code = uuid.uuid4(),
        size = size_3,
        price = price_3,
        longitude = longitude_3,
        latitude = latitude_3,
    )

    room_4 = Room(
        code = uuid.uuid4(),
        size = size_4,
        price = price_4,
        longitude = longitude_4,
        latitude = latitude_4,
    )
    ret_val = {'room': [room_1, room_2, room_3, room_4]}
    return ret_val

def test_room_read_all(domain_rooms):
    repo = mock.Mock()
    repo.read.return_value = domain_rooms

    result = room_read_all(repo)

    # Verificamos que no hemos usado parámetros al llamar a repo
    repo.read.assert_called_with()

    # Verificamos que el repo devuelve el valor esperado
    assert result == domain_rooms