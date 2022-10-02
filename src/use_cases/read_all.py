class ReadAll:
    @classmethod
    def read_all(self, repo, domain = 'room', verbose = False):
        return repo.read(domain, verbose)