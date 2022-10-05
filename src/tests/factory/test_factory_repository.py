import pytest

from ...factory.factory_repository import FactoryRepository
from ...factory.factory_simulator import FactorySimulator

from ...repository.repomem import RepoMem
from ...repository.repofile import RepoFile
from ...repository.reposql import RepoSql

@pytest.mark.factory
def test_create_repomem():
    repo_config = 'RepoMem' 
    config = FactorySimulator.create_repository_config(repo_config)    
    
    reals = FactoryRepository.create(repo_config, config)

    expected = RepoMem(config)

    assert reals.__class__ == expected.__class__

@pytest.mark.factory
def test_create_repofile():
    repo_config = 'RepoFile' 
    config = FactorySimulator.create_repository_config(repo_config)    
    
    reals = FactoryRepository.create(repo_config, config)

    expected = RepoFile(config)

    assert reals.__class__ == expected.__class__

@pytest.mark.factory
def test_create_reposql():
    repo_config = 'RepoSql' 
    config = FactorySimulator.create_repository_config(repo_config)    
    
    reals = FactoryRepository.create(repo_config, config)

    expected = RepoSql(config)

    assert reals.__class__ == expected.__class__
