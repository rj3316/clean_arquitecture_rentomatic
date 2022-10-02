from ...repository.repo_factory import RepoFactory
from ...domain.domainfactory import DomainFactory
from ...simulators.factorysimulator import FactorySimulator

def test_room_reposql_read_all():
    domain = 'room'
    sims = FactorySimulator.create_domain_dicts(domain)
    
    repo_detail = 'RepoSql'
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = RepoFactory.create(repo_detail, config)

    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.create(domain, sims)

    assert reals == expected
