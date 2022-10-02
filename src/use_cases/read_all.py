

class ReadAll:
    @classmethod
    def read_all(self, repo, domain, verbose = False):
        return repo.read(domain, verbose)