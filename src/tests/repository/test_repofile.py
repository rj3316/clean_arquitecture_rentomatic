from ...repository.repo_factory import RepoFactory
from ...domain.room import Room
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.infraestructure.simulator_file import file

def test_repository_read_all():
    sim_rooms = room_dicts()

    repo = RepoFactory.create('RepoFile', {'file': file})
    repo.write(sim_rooms)

    # import pdb; pdb.set_trace()
    domain = 'room'

    # Leemos el MemRepo
    rooms = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected_rooms = [Room.from_dict(i) for i in sim_rooms]

    repo.initialize()

    assert rooms == expected_rooms
