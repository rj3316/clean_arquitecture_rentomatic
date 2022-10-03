from ....repository.repo_factory import RepoFactory
from ....domain.domainfactory import DomainFactory
from ....simulators.factorysimulator import FactorySimulator

domain = 'hotel'
repo_detail = 'RepoMem'

def test_hotel_repomem_read_without_filters():
    sims = FactorySimulator.create_domain_dicts(domain)
    
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = RepoFactory.create(repo_detail, config)

    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # import pdb; pdb.set_trace()
    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.create(domain, sims)

    assert reals == expected

def test_hotel_repomem_read_with_filters_rooms_lt_12():
    filters = {'rooms__lt': 12}

    sims = FactorySimulator.create_domain_dicts(domain)
    sims_filt = FactorySimulator.create_domain_dicts(domain, filters = filters)
    
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = RepoFactory.create(repo_detail, config)

    repo.initialize(domain)
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain, filters)

    # Creamos una lista con lo que esperamos que el MemRepo nos devuelva
    expected = DomainFactory.create(domain, sims_filt)

    assert reals == expected