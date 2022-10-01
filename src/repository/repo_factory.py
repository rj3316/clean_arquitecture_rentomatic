from .repomem import RepoMem
from .repofile import RepoFile
from .reposql import RepoSql

class RepoFactory:
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
            