from ...domain.room import Room
from ...repository.repo_factory import RepoFactory
from ...simulators.domain.simulator_room import room_dicts

def test_repository_read_all():
    sim_rooms = room_dicts()

    # Instanciamos Repo (RepoMem) con una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoMem')
    repo.write(sim_rooms)

    domain = 'room'

    # Leemos el MemRepo
    rooms = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected_rooms = [Room.from_dict(i) for i in sim_rooms]

    assert rooms == expected_rooms

    repo.initialize()