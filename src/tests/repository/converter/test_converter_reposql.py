from ....factory.factory_repository import FactoryRepository
from ....factory.factory_domain import FactoryDomain
from ....factory.factory_simulator import FactorySimulator

domain = 'converter'
repo_detail = 'RepoSql'

def test_converter_reposql_read_without_filters():
    sims = FactorySimulator.create_domain_dicts(domain)
    
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = FactoryRepository.create(repo_detail, config)

    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = FactoryDomain.create(domain, sims)

    assert reals == expected

def test_converter_reposql_read_with_filters_rated_lt_25():
    filters = {'rated__lt': 25}

    sims = FactorySimulator.create_domain_dicts(domain)
    sims_filt = FactorySimulator.create_domain_dicts(domain, filters = filters)
    
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = FactoryRepository.create(repo_detail, config)

    repo.initialize(domain)
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain, filters)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = FactoryDomain.create(domain, sims_filt)

    assert reals == expected
