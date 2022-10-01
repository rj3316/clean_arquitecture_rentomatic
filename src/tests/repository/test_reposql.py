from ...domain.room import Room
from ...repository.repo_factory import RepoFactory
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.infraestructure.simulator_mysql import mysql

def test_repository_read_all():
    sim_rooms = room_dicts()

    domain = 'room'

    # Instanciamos RepoSql y escribimos una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoSql', {'ddbb_config': mysql})
    repo.write(domain, data = sim_rooms)


    # Leemos el RepoSql
    rooms = repo.read(domain)

    # Creamos una lista con lo que esperamos que el RepoSql nos devuelva
    expected_rooms = [Room.from_dict(i) for i in sim_rooms]

    repo.initialize(domain)

    assert rooms == expected_rooms

