from ...repository.repo_factory import RepoFactory
from ...domain.domainfactory import DomainFactory
from ...simulators.domain.simulator_room import room_dicts
from ...simulators.domain.simulator_hotel import hotel_dicts
from ...simulators.infraestructure.simulator_file import file

def test_repository_file_room_read_all():
    domain = 'room'
    sims = room_dicts()
    
    repo = RepoFactory.create('RepoFile', {'file': file})
    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.create(domain, sims)

    assert reals == expected

def test_repository_file_hotel_read_all():
    domain = 'hotel'
    sims = hotel_dicts()
    
    repo = RepoFactory.create('RepoFile', {'file': file})
    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.create(domain, sims)

    assert reals == expected
