from ...repository.repo_factory import RepoFactory
from ...domain.domainfactory import DomainFactory
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.domain.simulator_hotel import hotel_dicts

def test_repository_mem_room_read_all():
    domain = 'room'
    sims = room_dicts()
    
    # Instanciamos Repo (RepoMem) con una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoMem')
    repo.initialize()

    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.from_dicts(domain, sims)

    assert reals == expected

def test_repository_mem_hotel_read_all():
    domain = 'hotel'
    sims = hotel_dicts()

    # Instanciamos Repo (RepoMem) con una lista obtenida desde la "variable mock" room_dicts
    repo = RepoFactory.create('RepoMem')
    repo.initialize()

    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.from_dicts(domain, sims)

    assert reals == expected