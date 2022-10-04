from .factory import Factory
from ..repository.repomem import RepoMem
from ..repository.repofile import RepoFile
from ..repository.reposql import RepoSql

class FactoryRepository(Factory):
    @classmethod
    def create(cls, repo = None, config = None):
        ret_val = None
        if not isinstance(config, dict): config = None
        if isinstance(repo, str):
            if repo == 'RepoMem':
                ret_val = RepoMem(config)
            elif repo == 'RepoFile':
                ret_val = RepoFile(config)
            elif repo == 'RepoSql':
                ret_val = RepoSql(config)
            
        return ret_val
            