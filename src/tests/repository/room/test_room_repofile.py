from ....simulators.factorysimulator import FactorySimulator
from ....repository.repo_factory import RepoFactory
from ....domain.domainfactory import DomainFactory

domain = 'room'
repo_detail = 'RepoFile'

def test_room_repofile_read_without_filters():
    sims = FactorySimulator.create_domain_dicts(domain)
    
    config = FactorySimulator.create_repository_config(repo_detail)
    repo = RepoFactory.create(repo_detail, config)

    repo.initialize(domain)
    
    repo.write(domain, data = sims)

    # Leemos el MemRepo
    reals = repo.read(domain)

    # Creamos una lista con lo que esperamos que el repo nos devuelva
    expected = DomainFactory.create(domain, sims)

    assert reals == expected

def test_room_repofile_read_with_filters_price_gt_50():
    filters = {'price__gt': 50}

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

def test_room_repofile_read_with_filters_size_lr_100():
    filters = {'size__lr': 100}

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

def test_room_repofile_read_with_filters_price_gt_50_and_price_lt_150():
    filters = {'price__gt': 50, 'price__lt': 150}

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