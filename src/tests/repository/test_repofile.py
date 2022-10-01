from ...repository.repo_factory import RepoFactory
from ...domain.room import Room
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.infraestructure.simulator_file import file

def test_repository_file_read_all():
    sim_rooms = room_dicts()

    domain = 'room'
    repo = RepoFactory.create('RepoFile', {'file': file})
    
    repo.write(domain, data = sim_rooms)

    # Leemos el MemRepo
    rooms = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected_rooms = [Room.from_dict(i) for i in sim_rooms]

    repo.initialize()

    assert rooms == expected_rooms
