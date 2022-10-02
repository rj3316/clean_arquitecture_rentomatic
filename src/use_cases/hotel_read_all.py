class ReadAll:
    @classmethod
    def read_all(self, repo, domain = 'hotel', verbose = False):
        domain = 'hotel'
        return repo.read(domain, verbose)