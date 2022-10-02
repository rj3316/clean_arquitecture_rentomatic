from ...repository.repo_factory import RepoFactory
from ...domain.domainfactory import DomainFactory
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.domain.simulator_hotel import hotel_dicts
from ...simulators.infraestructure.simulator_mysql import mysql

def test_repository_sql_room_read_all():
    domain = 'room'
    sims = room_dicts()

    # Instanciamos RepoSql y escribimos una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoSql', {'ddbb_config': mysql})
    repo.initialize(domain)

    repo.write(domain, data = sims)

    # Leemos el RepoSql
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el RepoSql nos devuelva
    expected = DomainFactory.from_dicts(domain, sims)

    assert reals == expected

def test_repository_sql_hotel_read_all():
    domain = 'hotel'
    sims = hotel_dicts()

    # Instanciamos RepoSql y escribimos una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoSql', {'ddbb_config': mysql})
    repo.initialize(domain)

    repo.write(domain, data = sims)

    # Leemos el RepoSql
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el RepoSql nos devuelva
    expected = DomainFactory.from_dicts(domain, sims)

    assert reals == expected

