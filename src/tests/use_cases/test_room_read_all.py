from unittest import mock

from ...domain.room import Room
from ...use_cases.read_all import read_all
from ...simulators.domain.simulator_room import room_dicts

def test_room_read_all():
    sim_rooms = room_dicts()
    repo = mock.Mock()
    repo.read.return_value = [Room.from_dict(i) for i in sim_rooms]

    domain = 'room'
    result = read_all(repo, domain)

    # Verificamos que el repo devuelve el valor esperado
    assert result == [Room.from_dict(i) for i in sim_rooms]