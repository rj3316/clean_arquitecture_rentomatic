import pytest
from ....factory.factory_repository import FactoryRepository
from ....factory.factory_domain import FactoryDomain
from ....factory.factory_simulator import FactorySimulator

domain = 'hotel'
repo_detail = 'RepoFile'

@pytest.mark.repository
def test_hotel_repofile_read_without_filters():
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

@pytest.mark.repository
def test_hotel_repofile_read_with_filters_rooms_lt_12():
    filters = {'rooms__lt': 12}

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